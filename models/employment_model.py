# ==========================================
# DLSAU Alumni Tracking System
# models/employment_model.py
# ==========================================

import sqlite3

from config import DATABASE_PATH


class EmploymentModel:

    # ---------------------------------
    # Database Connection
    # ---------------------------------

    def connect(self):
        return sqlite3.connect(DATABASE_PATH)

    # ---------------------------------
    # Get Employment Information
    # ---------------------------------

    def get_employment(self, user_id):

        conn = self.connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM employment
            WHERE user_id=?
            """,
            (user_id,)
        )

        employment = cursor.fetchone()

        conn.close()

        if employment:
            return dict(employment)

        return None

    # ---------------------------------
    # Save / Update Employment
    # ---------------------------------

    def save_employment(

        self,

        user_id,

        employment_status,

        company,

        job_title,

        industry,

        work_location,

        salary_range

    ):

        conn = self.connect()

        cursor = conn.cursor()

        # Check if employment record already exists

        cursor.execute(

            """
            SELECT id
            FROM employment
            WHERE user_id=?
            """,

            (user_id,)

        )

        exists = cursor.fetchone()

        if exists:

            cursor.execute(

                """
                UPDATE employment

                SET

                    employment_status=?,
                    company=?,
                    job_title=?,
                    industry=?,
                    work_location=?,
                    salary_range=?

                WHERE user_id=?
                """,

                (

                    employment_status,

                    company,

                    job_title,

                    industry,

                    work_location,

                    salary_range,

                    user_id

                )

            )

        else:

            cursor.execute(

                """
                INSERT INTO employment(

                    user_id,

                    employment_status,

                    company,

                    job_title,

                    industry,

                    work_location,

                    salary_range

                )

                VALUES(?,?,?,?,?,?,?)
                """,

                (

                    user_id,

                    employment_status,

                    company,

                    job_title,

                    industry,

                    work_location,

                    salary_range

                )

            )

        conn.commit()

        conn.close()

    # ---------------------------------
    # Delete Employment
    # ---------------------------------

    def delete_employment(self, user_id):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(

            """
            DELETE
            FROM employment
            WHERE user_id=?
            """,

            (user_id,)

        )

        conn.commit()

        conn.close()