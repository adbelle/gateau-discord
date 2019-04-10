import random, datetime, sqlite3


def random_response_line():
    random_response = str(random.choice(list(open('response.txt')))[:-1])
    return random_response

def make_timestamp():
    gattimestamp = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    return gattimestamp

def read_single_definition(deftitle):
    conn = sqlite3.connect('gateau.db')
    c = conn.cursor()
    t = (deftitle,)
    c.execute('SELECT * FROM definitions WHERE title=?', t)
    data = c.fetchall()
    if str(data) == "[]":
        def_out = str("I don't have a definition for " + deftitle + ".")
    else:
        for row in data:
            def_out = "Definition for " + row[0] + ":```\n" + row[1] + "```"
    conn.close()
    return def_out

def read_pasta():
    conn = sqlite3.connect('gateau.db')
    c = conn.cursor()
    c.execute('SELECT * FROM pasta ORDER BY RANDOM() LIMIT 1')
    data = c.fetchall()
    for row in data:
        def_out = str(row[1])
    conn.close()
    return def_out
