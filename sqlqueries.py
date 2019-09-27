import sqlite3
user = "sarmistha"
conn = sqlite3.connect('3s.db')
c = conn.cursor()
# t = (user,)
# c.execute("CREATE TABLE documents_info (document text, swetha text, sarmistha text, ahamad text, location text)")


# c.execute("INSERT INTO documents_info VALUES ('trial.py','allowed','owner','','files/trial.py')")
# conn.commit()

# t = ("sarmistha", "trial.py",)
t = ("trial.py")
c.execute("SELECT * FROM documents_info WHERE document =?", t)



# t = ("nnnewfile.txt","nnnewfile.txt")
# c.execute("INSERT INTO documents_info VALUES (?,'allowed','owner','',?)", t)
# conn.commit()

# t = ('trial.py',)
# c.execute("DELETE FROM documents_info WHERE document=?", t)
# conn.commit()

# c.execute("SELECT * FROM documents_info")
res =  c.fetchall()
print res

conn.close()
