from contextlib import closing
import os
import random
import colorsys
import hashlib
import subprocess32
from urlparse import urlparse
from enum import Enum
import mysql.connector
from mysql.connector import errorcode
import pham.genbank
import pham.kclust
import pham.query
import pham.conserveddomain

def _default_callback(*args, **kwargs):
    pass

class DatabaseServer(object):
    def __init__(self, host, user, password='', pool_size=2, **kwargs):
        kwargs['host'] = host
        kwargs['user'] = user
        kwargs['password'] = password
        self._dbconfig = kwargs
        self._pool_size = pool_size

    @classmethod
    def from_url(cls, url, pool_size=2):
        result = urlparse(url)
        return cls(result.hostname, result.username, result.password, pool_size=pool_size)

    def get_credentials(self):
        host = self._dbconfig['host']
        user =  self._dbconfig['user']
        password = self._dbconfig['password']
        return host, user, password

    def get_connection(self, **kwargs):
        """Returns a mysql connection object from the connection pool.

        Raises: InvalidCredentials, NetworkError
        """
        config = self._dbconfig.copy()
        config.update(kwargs)
        return mysql.connector.connect(pool_size=self._pool_size, **config)

def check_create(server, id, genbank_files=None):
    """Check this create call for errors.

    Returns (success, errors)
    Where success is a boolean and errors is a list of strings.
    """
    observer = _CallbackObserver()

    try:
        success = create(server, id,
                        genbank_files=genbank_files,
                        cdd_search=False,
                        callback=observer.record_call,
                        commit=False)
    except DatabaseAlreadyExistsError as e:
        errors = []
        errors.append('Database name is already in use.')
        errors += observer.error_messages()
        return False, errors
    except Exception:
        delete(server, id)
        raise

    delete(server, id)

    return success, observer.error_messages()

def create(server, id, genbank_files=None, cdd_search=True, commit=True,
           callback=_default_callback):
    """

    Exceptions: DatabaseAlreadyExistsError
    """
    callback(CallbackCode.status, 'initializing database', 0, 2)
    with closing(server.get_connection()) as cnx:
        with closing(cnx.cursor()) as cursor:
            if _database_exists(cursor, id):
                raise DatabaseAlreadyExistsError
            cursor.execute("""
                           CREATE DATABASE {}
                           DEFAULT CHARACTER SET 'utf8'
                           """.format(id))
        cnx.commit()

    callback(CallbackCode.status, 'initializing database', 1, 2)
    try:
        with closing(server.get_connection(database=id)) as cnx:
            cnx.start_transaction()
            with closing(cnx.cursor()) as cursor:
                sql_script_path = os.path.join(_DATA_DIR, 'create_database.sql')
                _execute_sql_file(cursor, sql_script_path)
            cnx.commit()

        success = rebuild(server, id, None, genbank_files,
                          cdd_search=cdd_search,
                          callback=callback,
                          commit=commit)
    except Exception:
        delete(server, id)
        raise

    if not success:
        delete(server, id)

    return success

def delete(server, id):
    with closing(server.get_connection()) as cnx:
        with closing(cnx.cursor()) as cursor:
            cursor.execute('DROP DATABASE IF EXISTS {};'.format(id))
        cnx.commit()

def rebuild(server, id, organism_ids_to_delete=None, genbank_files_to_add=None,
            cdd_search=True, commit=True, callback=_default_callback):
    if organism_ids_to_delete is None:
        organism_ids_to_delete = []
    if genbank_files_to_add is None:
        genbank_files_to_add = []

    with closing(server.get_connection()) as cnx:
        if not pham.query.database_exists(cnx, id):
            raise DatabaseDoesNotExistError('No such database: {}'.format(id))

    # open and validate genbank files
    # also detect duplicate phages
    valid = True
    phage_id_to_filenames = {}
    duplicate_phage_ids = set()
    duplicate_phage_ids_on_server = set()
    if genbank_files_to_add is not None:
        for index, path in enumerate(genbank_files_to_add):
            callback(CallbackCode.status, 'validating genbank files', index, len(genbank_files_to_add))
            try:
                phage = pham.genbank.read_file(path)
            except IOError as e:
                valid = False
                callback(CallbackCode.file_does_not_exist, path)
                continue
            if phage.is_valid():
                # check for duplicate phages
                if phage.id in phage_id_to_filenames:
                    duplicate_phage_ids.add(phage.id)
                else:
                    phage_id_to_filenames[phage.id] = []
                phage_id_to_filenames[phage.id].append(phage.filename)
            else:
                valid = False
                for error in phage.errors:
                    callback(CallbackCode.genbank_format_error, error)

    with closing(server.get_connection(database=id)) as cnx:
        cnx.start_transaction()

        callback(CallbackCode.status, 'checking for conflicts', 0, 1)
        try:
            # check for phages which are already on the server
            for phage_id in phage_id_to_filenames:
                if pham.query.phage_exists(cnx, phage_id):
                    if phage_id not in organism_ids_to_delete:
                        duplicate_phage_ids_on_server.add(phage_id)

            if len(duplicate_phage_ids_on_server) or len(duplicate_phage_ids):
                valid = False
                for phage_id in duplicate_phage_ids_on_server:
                    filename = phage_id_to_filenames[phage_id][0]
                    callback(CallbackCode.duplicate_organism, phage_id, filename)
                for phage_id, filenames in phage_id_to_filenames.iteritems():
                    callback(CallbackCode.duplicate_genbank_files, phage_id, filenames)

            if not valid:
                cnx.rollback()
                return False

            new_gene_ids = []
            new_gene_sequences = []

            # update version number
            _increment_version(cnx)

            # delete organisms
            for index, phage_id in enumerate(organism_ids_to_delete):
                callback(CallbackCode.status, 'deleting organisms', index, len(organism_ids_to_delete))
                pham.query.delete_phage(cnx, phage_id)

            # upload genbank files
            if genbank_files_to_add is not None:
                for index, path in enumerate(genbank_files_to_add):
                    callback(CallbackCode.status, 'uploading organisms', index, len(genbank_files_to_add))
                    phage = pham.genbank.read_file(path)
                    if not phage.is_valid():
                        for error in phage.errors:
                            callback(CallbackCode.genbank_format_error, error)
                        cnx.rollback()
                        return False
                    # upload phage
                    try:
                        phage.upload(cnx)
                    except mysql.connector.errors.IntegrityError as e:
                        callback(CallbackCode.gene_id_already_exists, phage.id)
                        cnx.rollback()
                        return False
                    for gene in phage.genes:
                        new_gene_ids.append(gene.gene_id)
                        new_gene_sequences.append(gene.translation)

            if not commit:
                cnx.rollback()
                return True

            # calculate phams
            if len(new_gene_ids) or len(organism_ids_to_delete):
                with closing(cnx.cursor()) as cursor:
                    # download all genes
                    sequences = []
                    gene_ids = []

                    callback(CallbackCode.status, 'calculating phams', 0, 2)

                    cursor.execute('SELECT translation, GeneID FROM gene')
                    gene_rows = cursor.fetchall()
                    for sequence, gene_id in gene_rows:
                        sequences.append(sequence)
                        gene_ids.append(gene_id)

                    # cluster genes into phams
                    pham_id_to_gene_ids = pham.kclust.cluster(sequences, gene_ids,
                        on_first_iteration_done=lambda: callback(CallbackCode.status, 'calculating phams', 1, 2))

                    # calculate the colors for the phams
                    pham_id_to_color = _assign_colors(pham_id_to_gene_ids, cursor)

                    # clear old phams and colors from database
                    # write new phams and colors to database
                    cursor.execute('TRUNCATE TABLE pham')
                    cursor.execute('TRUNCATE TABLE pham_color')

                    for pham_id, gene_ids in pham_id_to_gene_ids.iteritems():
                        for gene_id in gene_ids:
                            cursor.execute('''
                                           INSERT INTO pham(GeneID, name)
                                           VALUES (%s, %s)
                                           ''', (gene_id, pham_id)
                                           )

                    for pham_id, color in pham_id_to_color.iteritems():
                        cursor.execute('''
                                       INSERT INTO pham_color(name, color)
                                       VALUES (%s, %s)
                                       ''', (pham_id, color))

            if cdd_search and len(new_gene_ids):
                callback(CallbackCode.status, 'searching conserved domain database', 0, 1)
                # search for genes in conserved domain database
                # only search for new genes
                pham.conserveddomain.find_domains(cnx, new_gene_ids, new_gene_sequences)

        except Exception:
            cnx.rollback()
            raise

        cnx.commit()

    return True

def load(server, id, filepath):
    """Load an SQL dump into the database.

    Also migrates to the new schema if needed.
    """
    with closing(server.get_connection()) as cnx:
        if pham.query.database_exists(cnx, id):
            raise DatabaseAlreadyExistsError('Database {} already exists.'.format(id))
        
        with closing(cnx.cursor()) as cursor:
            cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(id))
        cnx.commit()

    with closing(server.get_connection(database=id)) as cnx:
        with closing(cnx.cursor()) as cursor:
            _execute_sql_file(cursor, filepath)
        _update_schema(cnx)
        cnx.commit()

def export(server, id, filepath):
    """Saves a SQL dump of the database to the given file.

    Also creates <filename>.version and <filename>.md5sum files in the same
    directory.
    """
    directory = os.path.dirname(filepath)
    base_path = '.'.join(filepath.split('.')[:-1]) # remove extension from filename
    version_filename = '{}.version'.format(base_path)
    checksum_filename = '{}.md5sum'.format(base_path)

    with closing(server.get_connection()) as cnx:
        if not pham.query.database_exists(cnx, id):
            raise DatabaseDoesNotExistError('No such database: {}'.format(id))

    if os.path.exists(filepath):
        raise IOError('File already exists: {}'.format(filepath))
    if os.path.exists(version_filename):
        raise IOError('File already exists: {}'.format(version_filename))
    if os.path.exists(checksum_filename):
        raise IOError('File already exists: {}'.format(checksum_filename))

    if directory != '' and not os.path.exists(directory):
        os.makedirs(directory)

    # export database to sql file using mysqldb command line program
    host, user, password = server.get_credentials()
    command = ['mysqldump', '--host', host, '--user', user]
    if password != '' and password is not None:
        command += ['--password', password]
    command.append(id)

    with open(filepath, 'w') as output_file:
        with open(os.devnull, 'wb') as DEVNULL:
            subprocess32.check_call(command, stdout=output_file, stderr=DEVNULL)

    # write .version file
    with closing(server.get_connection(database=id)) as cnx:
        version_number = pham.query.version_number(cnx)

    with open(version_filename, 'w') as out_file:
        out_file.write('{}\n'.format(version_number))

    # calculate checksum
    m = hashlib.md5()
    with open(filepath, 'rb') as sql_file:
        while True:
            data = sql_file.read(8192)
            if data == '':
                break
            m.update(data)

    # write .md5sum file
    checksum = m.hexdigest()
    with open(checksum_filename, 'w') as out_file:
        out_file.write('{}  {}\n'.format(checksum, filepath))

def _update_schema(cnx):
    """Migrate databases from the old Phamerator schema.

    The new schema is backwards compatible with Phamerator.
    The changes made are as follows:

    Add ON DELETE CASCADE constraints
    Increase VARCHAR length
    TRUNCATE TABLE scores_summary, node
    DROP TABLE pham_history, pham_old
    CREATE TABLE version
    """
    with closing(cnx.cursor()) as cursor:
        # add version table
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS version (
                         id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                         version int NOT NULL
                       )''')
        cursor.execute('SELECT * FROM version')
        if len(cursor.fetchall()) == 0:
            cursor.execute('''INSERT INTO version (version)
                              VALUES (0)
                            ''')

        # increase VARCHAR length
        # select character_maximum_length from information_schema.columns where table_schema = 'test_database' and table_name = 'gene' and column_name = 'name';
        cursor.execute('''
                       SELECT character_maximum_length
                       FROM information_schema.columns
                       WHERE table_schema IN (SELECT database())
                        AND table_name = 'gene'
                        AND column_name = 'Name'
                       ''')
        if cursor.fetchall()[0][0] != 127:
            cursor.execute('ALTER TABLE domain MODIFY hit_id VARCHAR(127)')
            cursor.execute('ALTER TABLE domain MODIFY Name VARCHAR(127)')
            cursor.execute('ALTER TABLE gene MODIFY GeneID VARCHAR(127)')
            cursor.execute('ALTER TABLE gene MODIFY PhageID VARCHAR(127)')
            cursor.execute('ALTER TABLE gene MODIFY Name VARCHAR(127)')
            cursor.execute('ALTER TABLE gene MODIFY LeftNeighbor VARCHAR(127)')
            cursor.execute('ALTER TABLE gene MODIFY RightNeighbor VARCHAR(127)')
            cursor.execute('ALTER TABLE gene_domain MODIFY GeneID VARCHAR(127)')
            cursor.execute('ALTER TABLE gene_domain MODIFY hit_id VARCHAR(127)')
            cursor.execute('ALTER TABLE node MODIFY hostname VARCHAR(127)')
            cursor.execute('ALTER TABLE phage MODIFY PhageID VARCHAR(127)')
            cursor.execute('ALTER TABLE phage MODIFY Name VARCHAR(127)')
            cursor.execute('ALTER TABLE phage MODIFY Isolated VARCHAR(127)')
            cursor.execute('ALTER TABLE phage MODIFY HostStrain VARCHAR(127)')
            cursor.execute('ALTER TABLE pham MODIFY GeneID VARCHAR(127)')
            cursor.execute('ALTER TABLE scores_summary MODIFY query VARCHAR(127)')
            cursor.execute('ALTER TABLE scores_summary MODIFY subject VARCHAR(127)')

        # add ON DELETE CASCADE constraints
        cursor.execute('''
                       SELECT COUNT(delete_rule)
                       FROM information_schema.referential_constraints
                       WHERE constraint_schema IN (SELECT database())
                        AND delete_rule = 'CASCADE'
                       ''')
        if cursor.fetchall()[0][0] < 6:
            _migrate_foreign_key(cursor, 'gene', 'gene_ibfk_1', 'PhageID', 'phage', 'PhageID')
            _migrate_foreign_key(cursor, 'gene_domain', 'gene_domain_ibfk_1', 'GeneID', 'gene', 'GeneID')
            _migrate_foreign_key(cursor, 'gene_domain', 'gene_domain_ibfk_2', 'hit_id', 'domain', 'hit_id')
            _migrate_foreign_key(cursor, 'pham', 'pham_ibfk_2', 'GeneID', 'gene', 'GeneID')
            _migrate_foreign_key(cursor, 'scores_summary', 'scores_summary_ibfk_1', 'query', 'gene', 'GeneID')
            _migrate_foreign_key(cursor, 'scores_summary', 'scores_summary_ibfk_2', 'subject', 'gene', 'GeneID')

        # truncate unnecessary tables
        # some tables are truncated instead of deleted to maintain backwards compatibility
        cursor.execute('TRUNCATE TABLE scores_summary')
        cursor.execute('TRUNCATE TABLE node')

        # delete unnecessary tables
        cursor.execute('DROP TABLE IF EXISTS pham_old')
        cursor.execute('DROP TABLE IF EXISTS pham_history')

def _migrate_foreign_key(cursor, this_table, constraint, this_feild, other_table, other_feild):
    try:
        cursor.execute('ALTER TABLE {} DROP FOREIGN KEY {}'.format(this_table, constraint))
    except mysql.connector.errors.Error as e:
        if e.errno == errorcode.ER_ERROR_ON_RENAME:
            # the constraint did not already exist
            pass
        else:
            raise

    cursor.execute('''
                   ALTER TABLE {}
                   ADD CONSTRAINT {} FOREIGN KEY ({}) REFERENCES {} ({})
                   ON UPDATE CASCADE
                   ON DELETE CASCADE
                   '''.format(this_table, constraint, this_feild, other_table, other_feild))

def _increment_version(cnx):
    with closing(cnx.cursor()) as cursor:
        cursor.execute('''
                       UPDATE version
                       SET version=version+1
                       ''')

def _assign_colors(pham_id_to_gene_ids, cursor):
    # fetch genes which previously had no pham assignment
    cursor.execute('''
                SELECT gene.GeneID
                FROM gene
                JOIN pham
                ON gene.GeneID = pham.GeneID
                WHERE pham.name is NULL
                ''')
    new_genes = { row[0] for row in cursor }

    # fetch pham color assignments
    cursor.execute('''
                SELECT name, color
                FROM pham_color
                ''')
    old_pham_to_color = {}
    for pham_id, color in cursor:
        old_pham_to_color[pham_id] = color

    pham_id_to_color = {}

    # calculate a color for each pham
    # copy over the old color for phams which are the same as old phams
    # if a pham gained a few new genes, its color is also copied
    if len(old_pham_to_color):
        for pham_id, gene_ids in pham_id_to_gene_ids.iteritems():
            found = set()
            genes = set(gene_ids)
            # exclude genes which previously had no pham assignment
            for gene_id in new_genes:
                if gene_id in genes:
                    found.insert(gene_id)
                    genes.remove(gene_id)
            new_genes -= found
            
            pham_id_to_color[pham_id] = old_pham_to_color.get(frozenset(genes), _make_color(gene_ids))
    else:
        for pham_id, gene_ids in pham_id_to_gene_ids.iteritems():
            pham_id_to_color[pham_id] = _make_color(gene_ids)
    return pham_id_to_color

def _make_color(gene_ids):
    if len(gene_ids) == 1:
        return '#FFFFFF'

    hue = random.uniform(0, 1)
    sat = random.uniform(0.5, 1)
    val = random.uniform(0.8, 1)

    red, green, blue = colorsys.hsv_to_rgb(hue, sat ,val)
    hexcode = '#%02x%02x%02x' % (red * 255, green * 255, blue * 255)
    return hexcode
    
def _database_exists(cursor, id):
    """Returns True if the database exists.
    """

    cursor.execute('SHOW DATABASES LIKE %s;', (id,))
    if len(cursor.fetchall()) == 0:
        return False
    return True

def _execute_sql_file(cursor, filepath):
    with open(filepath, 'r') as sql_script_file:
        try:
            cursors = cursor.execute(sql_script_file.read(), multi=True)
            for result_cursor in cursors:
                for row in result_cursor:
                    pass
        except mysql.connector.Error as err:
            raise DatabaseError(err)

class _CallbackObserver(object):
    def __init__(self):
        self.calls = []

    def record_call(self, code, *args, **kwargs):
        self.calls.append((code, args, kwargs))

    def error_messages(self):
        messages = []
        genbank_format_errors = 0
        for code, args, kwargs in self.calls:
            if code == CallbackCode.genbank_format_error:
                genbank_format_errors += 1
            elif code != CallbackCode.status:
                messages.append(message_for_callback(code, *args, **kwargs))

        if genbank_format_errors:
            messages.append('{} errors occurred while validating genbank files.'.format(genbank_format_errors))
        
        return messages

def message_for_callback(code, *args, **kwargs):
    message = None
    if code == CallbackCode.genbank_format_error:
        phage_error = args[0]
        message = 'Error validating genbank file:' + phage_error.message()
    elif code == CallbackCode.duplicate_organism:
        phage_id = args[0]
        message = 'Adding phages resulted in duplicate phage. ID: {}'.format(phage_id)
    elif code == CallbackCode.duplicate_genbank_files:
        phage_id = args[0]
        message = 'The same genbank file occurs twice. Phage ID: {}'.format(phage_id)
    elif code == CallbackCode.file_does_not_exist:
        message = 'Unable to find uploaded genbank file.'
    elif code == CallbackCode.gene_id_already_exists:
        phage_id = args[0]
        message = 'Unable to add phage: ID: {}. A gene in this phage occurs elsewhere in the database.'.format(gene_id)
    return message

_DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')

CallbackCode = Enum('status',
                    'genbank_format_error',
                    'duplicate_organism',
                    'duplicate_genbank_files',
                    'file_does_not_exist',
                    'gene_id_already_exists')

class DatabaseError(Exception):
    pass

class InvalidCredentials(DatabaseError):
    pass

class DatabaseAlreadyExistsError(DatabaseError):
    pass

class DatabaseDoesNotExistError(DatabaseError):
    pass