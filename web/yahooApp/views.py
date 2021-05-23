from datetime import datetime, date

from flask import Response
from yahooApp.serializers import SymbolSchema

from yahooApp.models import Symbol, create_table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from yahooApp.config import SQLALCHEMY_DATABASE_URI

import pandas as pd
import csv
import io
import numpy as np
import json
import requests as rq
from flask_restful import Resource


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True


class HelloWorld(Resource):
    def __init__(self):
        super().__init__()
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)
        create_table(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.conn = self.engine.raw_connection()
        self.cur = self.conn.cursor()

    @staticmethod
    def validation_data(item):
        try:
            return float(item)
        except ValueError:
            return 0

    def get_csv(self, csv_from_url, symbol_db):
        reader = csv.DictReader(io.StringIO(csv_from_url))
        self.cur.execute('''SELECT coalesce(max(id)+1, 1) FROM history;''')
        max_id = self.cur.fetchone()[0]
        df = pd.DataFrame([
            {
                "symbol_id": symbol_db.id,
                "date": date.fromisoformat(item['Date']),
                "open": self.validation_data(item['Open']),
                "high": self.validation_data(item['High']),
                "low": self.validation_data(item['Low']),
                "close": self.validation_data(item['Close']),
                "adj_close": self.validation_data(item['Adj Close']),
                "volume": self.validation_data(item['Volume'])
            } for idx, item in enumerate(reader)
        ])
        df.index = np.arange(max_id, len(df) + max_id)
        output = io.StringIO()
        df.to_csv(output, sep='\t', header=False, index_label='id')
        output.seek(0)
        return output

    def get(self, symbol):
        symbol = symbol.upper()
        url_yahoo = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1=0&period2=' \
                    f'{int(datetime.now().timestamp() * 1000)}&interval=1d&events=history&includeAdjustedClose=true'
        req = rq.get(url_yahoo)
        if req.status_code == 404:
            return json.dumps({'status': f'Company with symbol \"{symbol}\" not found'})
        else:
            symbol_db, _ = get_or_create(self.session, Symbol, symbol=symbol)
            output = self.get_csv(csv_from_url=req.text, symbol_db=symbol_db)
            self.cur.execute(f'''
                                SELECT count(id) FROM history 
                                WHERE symbol_id = '{symbol_db.id}'; ''')
            if self.cur.fetchone()[0] == 0:
                self.cur.copy_from(output, 'history', null="")
                self.conn.commit()
            else:
                self.cur.copy_from(output, 'history_tmp', null="")
                self.conn.commit()
                self.cur.execute(''' 
                                INSERT INTO history
                                SELECT * FROM history_tmp
                                ON CONFLICT (date, symbol_id)
                                DO NOTHING
                                ''')
                self.cur.execute('DROP TABLE history_tmp;')
                self.conn.commit()

            get_symbol = self.session.query(Symbol).filter(Symbol.symbol == symbol).one()
            data_schema = SymbolSchema()
            return data_schema.dump(get_symbol)


class DownloadFile(Resource):
    def get(self, symbol):
        return Response(
            json.dumps(HelloWorld().get(symbol)),
            mimetype='application/json',
            headers={
                'Content-Disposition': f'attachment;filename={symbol}.json'
            })