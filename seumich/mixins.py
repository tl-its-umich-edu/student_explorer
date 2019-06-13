class SeumichDataMixin(object):
    def valid_date_or_none(self, dt):
        if dt is None:
            return None;
        elif dt.id < 0:
            return None
        else:
            return dt

    def aggrate_relationships(self, collection, primary, relationship,
                              relationship_plural=None):
        if relationship_plural is None:
            relationship_plural = relationship + 's'

        tmp = {}
        for entry in collection:
            pri = getattr(entry, primary)
            if pri not in list(tmp.keys()):
                tmp[pri] = []
            rel = getattr(entry, relationship)
            tmp[pri].append(rel)

        aggrated = []
        for (pri, rels) in list(tmp.items()):
            aggrated.append({primary: pri, relationship_plural: rels})

        return aggrated
