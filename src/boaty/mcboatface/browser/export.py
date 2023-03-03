from zope.publisher.browser import BrowserView
from boaty.mcboatface.database import get_connection
from plone import api
import logging
import transaction
logger = logging.getLogger('export')


class ExportStudentToMySQL(BrowserView):
    def __call__(self):
        students = api.content.find(portal_type='Student', sort_on='created')
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute('drop table if exists students')
                create_table_sql = """CREATE TABLE `students` (
                    `id` int(11) NOT NULL AUTO_INCREMENT,
                    `studentName` varchar(255) COLLATE utf8_bin NULL,
                    `age` varchar(255) COLLATE utf8_bin NULL,
                    `gender` varchar(255) COLLATE utf8_bin NULL,
                    `ageBelow25` varchar(255) COLLATE utf8_bin NULL,
                    PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
                AUTO_INCREMENT=1 ;
                """
                cursor.execute(create_table_sql)
                connection.commit()
                for student in students:
                    obj = student.getObject()
                    data = {
                        'studentName': obj.studentName,
                        'age': obj.age,
                        'gender': obj.gender,
                        'ageBelow25': obj.ageBelow25()
                        }
                    sql = """INSERT INTO `students` 
                    (`studentName`, `age`, `gender`, `ageBelow25`) 
                    VALUES ('%(studentName)s', '%(age)s', '%(gender)s', '%(ageBelow25)s')""" % data 
                    logger.info(sql)
                    logger.info((obj.studentName, str(obj.age), obj.gender))
                    cursor.execute(sql)
                    connection.commit()
        return 'done'
