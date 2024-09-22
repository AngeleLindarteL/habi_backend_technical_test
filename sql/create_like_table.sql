CREATE TABLE IF NOT EXISTS like_history (
   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,         
   property_id INTEGER NOT NULL,            
   user_id INTEGER NOT NULL,                
   created_at VARCHAR(256) NOT NULL,            
   CONSTRAINT FK_property FOREIGN KEY (property_id) REFERENCES property(id)  
   CONSTRAINT FK_user FOREIGN KEY (user_id) REFERENCES user(id)  
);