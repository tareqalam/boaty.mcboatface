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
                    PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
                AUTO_INCREMENT=1 ;
                """
                cursor.execute(create_table_sql)
                connection.commit()
                for student in students:
                    obj = student.getObject()
                    sql = "INSERT INTO `students` (`studentName`, `age`, `gender`) VALUES ('%s', '%s', '%s')" % (obj.studentName, str(obj.age), obj.gender)
                    logger.info(sql)
                    logger.info((obj.studentName, str(obj.age), obj.gender))
                    cursor.execute(sql)
                    connection.commit()
        return 'done'
