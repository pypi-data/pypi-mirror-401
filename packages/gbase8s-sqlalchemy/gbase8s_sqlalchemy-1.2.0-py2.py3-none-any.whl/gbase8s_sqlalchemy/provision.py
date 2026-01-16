
from sqlalchemy.testing.provision import temp_table_keyword_args


@temp_table_keyword_args.for_db("gbase8s")
def _gbase8s_temp_table_keyword_args(cfg, eng):
    if eng.dialect.sqlmode == 'mysql':
        keyword = 'TEMPORARY'
    elif eng.dialect.sqlmode == 'gbase':
        keyword = 'TEMP'
    else:
        keyword = 'GLOBAL TEMPORARY'
    return {
        "prefixes": [keyword]
    }