import asyncio
import aiomysql
from config import Config

class Db:
    """Подключение и работа с базой данных"""
    ADMINS_TABLE = 'admins'

    def __init__(self) -> None:
        self._user = Config.PUSER
        self._host = Config.PHOST
        self._pswd = Config.PPASSWORD
        self._db = Config.PDATABASE


    async def get_connection(self):
        try:
            connect = await aiomysql.connect(self._host, self._user, self._pswd, self._db)
            return connect
        except Exception as e:
            print('error Db->get_connection()', e)
            


    async def createTableSession(self) -> bool:
        try:
            conn = await self.get_connection()
            async with conn.cursor() as cur:
                await cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS `session` (
                    `sis` INT(11) NOT NULL AUTO_INCREMENT,
                    `user` INT(11) NULL DEFAULT NULL,
                    `token` VARCHAR(550) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
                    PRIMARY KEY (`sis`) USING BTREE,
                    UNIQUE INDEX `sis` (`sis`) USING BTREE,
                    INDEX `user` (`user`) USING BTREE,
                    CONSTRAINT `user` FOREIGN KEY (`user`) REFERENCES `admins` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
                )
                COMMENT='Сессии'
                COLLATE='utf8mb4_general_ci'
                ENGINE=InnoDB ;
                """)
                await conn.commit()
                return True
        except Exception as e:
            print('error in Db->createTableSession()', e)
            return False
        finally:
            conn.close()



    async def add_admin_user(self, name, id):
        try:
            conn = await self.get_connection()
            async with conn.cursor() as cur:
                await cur.execute(f""" 
                        INSERT INTO {Db.ADMINS_TABLE}(name, telegram_id)
                        VALUES(%s, %s);
                """, [name, id])
                await conn.commit()

        except Exception as e:
            print('error in Db->add_admin_user()', e)
        finally:
            conn.close()


    async def get_all_usrs(self):
        try:
            conn = await self.get_connection()
            async with conn.cursor() as cur:
                await cur.execute(f"SELECT * FROM {Db.ADMINS_TABLE};")
                result = await cur.fetchall()
                await conn.commit()
                return result
        except Exception as e:
            print('error in Db->get_all_usrs()', e)
        finally:
            conn.close()


    async def del_user_by_id(self, id: str)-> bool:
        try:
            conn = await self.get_connection()
            async with conn.cursor() as cur:
                
                result = await cur.execute(f'DELETE FROM {Db.ADMINS_TABLE} WHERE telegram_id={id.strip()};')
                await conn.commit()
                if bool(result):
                    return True
                return False

        except Exception as e:
            print('error in Db->skeleton()', e)
            return False
        finally:
            conn.close()



    async def skeleton(self):
        try:
            conn = await self.get_connection()
            async with conn.cursor() as cur:
                pass

        except Exception as e:
            print('error in Db->skeleton()', e)
        finally:
            conn.close()
    


    async def is_auth(self, some_id) -> list:
        """return [id, name] or []"""
        try:
            conn = await self.get_connection()
            async with conn.cursor() as cur:
                await cur.execute(f"SELECT * FROM {Db.ADMINS_TABLE};")
                result = await cur.fetchone()
                _, name, id = result
                await conn.commit()
                
                if some_id == id:
                    return [id, name]
                return []
            
        except Exception as e:
            print('error in Db->is_auth()', e)
        finally:
            conn.close()
            
            
