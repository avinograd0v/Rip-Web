# -*- coding: utf-8 -*-
from django.db import models, connection


class SearchQuerySet(models.query.QuerySet):
    def __init__(self, fields=None, **kwargs):
        super(SearchQuerySet, self).__init__(**kwargs)
        self.search_fields = fields

    def get_query_set(self, query, columns, mode):
        fulltext_columns = ', '.join(columns)
        where_expression = ('MATCH({}) AGAINST("%s" {})'.format(fulltext_columns, mode))

        return self.extra(where=[where_expression], params=[query])

    def search(self, query, fields=None, mode=None):
        meta = self.model._meta
        quote_name = connection.ops.quote_name
        seperator = models.constants.LOOKUP_SEP

        columns = set()
        related_fields = set()

        fields = self.search_fields if fields is None else fields

        for field in fields:
            if seperator in field:
                field, rfield = field.split(seperator)
                rmodel = meta.get_field(field).related_model
                rmeta = rmodel._meta
                table = rmeta.db_table
                column = rmeta.get_field(rfield).column
                related_fields.add(field)
            else:
                table = meta.db_table
                column = meta.get_field(field).column

            columns.add('{}.{}'.format(quote_name(table), quote_name(column)))

        print(columns)

        if mode is None and any(x in query for x in '+-><()*"'):
            mode = 'BOOLEAN'

        if mode is None:
            mode = ''
        else:
            mode = 'IN {} MODE'.format(mode)

        query_set = self.get_query_set(query, columns, mode)

        if related_fields:
            query_set = query_set.select_related(','.join(related_fields))

        return query_set

    def count(self):
        return self.__len__()


class SearchManager(models.Manager):
    query_set = SearchQuerySet

    def __init__(self, fields=None):
        super(SearchManager, self).__init__()
        self.search_fields = fields

    def get_query_set(self):
        return self.query_set(model=self.model, fields=self.search_fields)

    def search(self, query, **kwargs):
        return self.get_query_set().search(query, **kwargs)
