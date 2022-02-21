import json

raw_ontology = json.load(open("resources/ontology.json"))

parent_id = {}
for i in raw_ontology:
    if i['child_ids']:
        parent_id.update({node: i['id'] for node in i['child_ids']})

raw_ontology = [{**i, **{"parent_id": parent_id.get(i['id'])}} for i in raw_ontology]


def get_data(result_list):
    id2name = {i['id']: i['name'] for i in result_list}
    id2example = {
        i['id']: [
            "http://www.youtube.com/embed/{}?enablejsapi=1&origin=http://example.com".format(j.split('/')[-1])
            for j in i['positive_examples']
        ] for i in result_list
    }
    id2tooltip = {i['id']: i['description'] for i in result_list}
    id2folder = {i['id']: True if i["child_ids"] else False for i in result_list}
    links_dict = {}
    for i in result_list:
        links_dict[i['parent_id']] = links_dict.get(i['parent_id'], []) + [i['id']]

    def get_nodes(node):
        d = {}
        d['key'] = node
        d['title'] = id2name.get(node)
        d['folder'] = id2folder.get(node)
        d['tooltip'] = id2tooltip.get(node)
        d['sample'] = id2example.get(node)
        children = get_children(node)
        if children:
            d['children'] = [get_nodes(child) for child in children]
        return d

    def get_children(node):
        return links_dict.get(node, [])
    tree = get_nodes(None)
    return tree['children']


if __name__ == '__main__':
    import json

    json.dump(
        obj=get_data(raw_ontology),
        fp=open(
            file='./resources/ontology_fancytree.json',
            mode='w'
        )
    )

