import sqlite3

class BotDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id, username, first_name, last_name):
        self.cursor.execute("INSERT INTO `users` (`user_id`, `username`, `first_name`, `last_name`) VALUES (?,?,?,?)", (user_id,username,first_name,last_name))
        return self.conn.commit()
    
    def add_crop(self, user_id, crop_name, crop_quantity_produced, crop_expense, crop_price):
        self.cursor.execute("INSERT INTO `crops` (`user_id`, `crop_name`, `crop_quantity_produced`, `crop_expense`, `crop_price`) VALUES (?, ?, ?, ?, ?)",
            (user_id,
            crop_name,
            crop_quantity_produced,
            crop_expense,
            crop_price))
        return self.conn.commit()
    
    def add_weather_soil(self, crop_id, temperature, pressure, soil_moisture, humidity, radiation, precipitation):
        self.cursor.execute("INSERT INTO `weather_and_soil_of_crop` (`crop_id`, `temperature`, `pressure`, `soil_moisture`, `humidity`, `radiation`, `precipitation`) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (crop_id,
            temperature,
            pressure,
            soil_moisture,
            humidity,
            radiation,
            precipitation))
        return self.conn.commit()

    def get_crop(self, user_id):
        result = self.cursor.execute("SELECT * FROM `crops` WHERE `user_id` = ?", (user_id,))
        fetchall = result.fetchall()
        final_array = []

        for idx, item in enumerate(fetchall, start=1):
            formatted_item = ', '.join(str(i).replace("'", "") for i in item)
            final_array.append(f"<b>{idx}.</b> {formatted_item}")

        result_string = '\n'.join(final_array)
        return result_string

    def update_crop(self, crop_id, user_id, crop_name, crop_quantity_produced, crop_expense, crop_price):
        self.cursor.execute("UPDATE `crops` SET `crop_name` = ?, `crop_quantity_produced` = ?, `crop_expense` = ?, `crop_price` = ? WHERE `id` = ? AND `user_id` = ?",
            (crop_name,
            crop_quantity_produced,
            crop_expense,
            crop_price,
            crop_id,
            user_id))
        return self.conn.commit()
    
    def financial_analysis(self, user_id):
        result = self.cursor.execute("SELECT id, crop_name, crop_quantity_produced, crop_expense, crop_price FROM `crops` WHERE `user_id` = ?", (user_id,))
        fetchall = result.fetchall()
        final_array = []

        for idx, (id, crop_name, crop_quantity_produced, crop_expense, crop_price) in enumerate(fetchall, start=1):
            crop_quantity_produced = int(crop_quantity_produced)
            crop_price = float(crop_price)
            crop_expense = float(crop_expense)
            total_expense = crop_expense
            total_profit = crop_quantity_produced * crop_price - total_expense

            formatted_item = f"<b>{idx}.</b> Crop ID: {id}, Crop Name: {crop_name}, Total Expense: {total_expense}$, Net Profit: {total_profit}$"
            final_array.append(formatted_item)

        result_string = '\n'.join(final_array)
        return result_string
    
    def get_weatherandsoil(self):
        result = self.cursor.execute("SELECT * FROM `weather_and_soil_of_crop`")
        fetchall = result.fetchall()
        final_array = []

        for idx, item in enumerate(fetchall, start=1):
            formatted_item = ', '.join(str(i).replace("'", "") for i in item)
            final_array.append(f"<b>{idx}.</b> {formatted_item}")

        result_string = '\n'.join(final_array)
        return result_string


    def close(self):
        self.connection.close()