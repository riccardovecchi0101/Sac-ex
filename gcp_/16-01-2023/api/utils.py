from datetime import datetime

def date_from_str(d):
    try: return datetime.strptime(d, '%d-%m-%Y')
    except: return None
def str_from_date(d):
    return d.strftime('%d-%m-%Y')
3