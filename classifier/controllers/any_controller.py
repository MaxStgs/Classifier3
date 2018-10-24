import connexion
import six

from classifier.models.create_element import CreateElement  # noqa: E501
from classifier.models.element_details import ElementDetails  # noqa: E501
from classifier.models.update_element_details import UpdateElementDetails  # noqa: E501
from classifier import util
from flask import make_response, abort
from classifier.config import db
from classifier.Element import Element, ElementSchema


def create_element(createElement):  # noqa: E501
    """create_element

    Create Element  # noqa: E501

    :param createElement: Create element request. 
    :type createElement: dict | bytes

    :rtype: ElementDetails
    """
    # if connexion.request.is_json:
    #      createElement = CreateElement.from_dict(connexion.request.get_json())  # noqa: E501

    # id = createElement.get("id")
    #
    # existing_element = (
    #     Element.query.filter(Element.id == id)
    #         .one_or_none()
    # )
    #
    # if existing_element is None:
    #     schema = ElementSchema()
    #     createElement = None
    #     new_element = schema.load(createElement, session=db.session).data
    #
    #     db.session.add(new_element)
    #     db.session.commit()
    #
    #     data = schema.dump(new_element).data
    #
    #     return data, 201
    # else:
    #     abort(
    #         409,
    #         "Element {id} exists already".format(
    #             id=id
    #         ),
    #     )

    schema = ElementSchema()
    # new_element = schema.load(createElement, session=db.session).data
    # new_element.id = None  # It is my bike for ride

    new_element = Element(
        elementName=createElement['elementName'],
        isEnd=createElement['isEnd'],
        isIndexed=createElement['isIndexed'],
        isRoot=createElement['isRoot'],
        parentElementId=createElement['parentElementId']
    )

    db.session.add(new_element)
    db.session.commit()
    data = schema.dump(new_element).data
    return data, 201


def delete_element(elementId):  # noqa: E501
    """delete_element

    Delete element by Id  # noqa: E501

    :param elementId: Unique identifier of Element 
    :type elementId: int

    :rtype: None
    """

    element = (Element.query.filter(Element.id == elementId).one_or_none())

    if element is not None:
        if not is_child_exists(elementId):
            db.session.delete(element)
            db.session.commit()
            return make_response("Element {id} deleted".format(id=elementId), 200)
        else:
            abort(404, "Element with {id} can't be deleted because have some childrens".format(id=elementId), )
    else:
        abort(404, "Element {id} not found".format(id=elementId), )


def get_element(elementId):  # noqa: E501
    """get_element

    Get Element details  # noqa: E501

    :param elementId: Unique identifier of Element 
    :type elementId: int

    :rtype: ElementDetails
    """

    element = Element.query.filter(Element.id == elementId).one_or_none()
    if element is not None:
        element_schema = ElementSchema()
        data = element_schema.dump(element).data
        return data
    else:
        abort(404, "Element not found for Id: {element_id}".format(element_id=elementId), )


def list_elements():  # noqa: E501
    """list_elements

    List of elements  # noqa: E501


    :rtype: List[ElementDetails]
    """
    elements = Element.query.order_by(Element.id).all()
    element_schema = ElementSchema(many=True)
    data = element_schema.dump(elements).data
    return data


def update_element(elementId, elementDetails):  # noqa: E501
    """update_element

     # noqa: E501

    :param elementId: Unique identifier of Element 
    :type elementId: int
    :param elementDetails: Update element details request 
    :type elementDetails: dict | bytes

    :rtype: None
    """
    # if connexion.request.is_json:
    #     elementDetails = UpdateElementDetails.from_dict(connexion.request.get_json())  # noqa: E501
    element = Element.query.filter(Element.id == elementId).one_or_none()

    if element is not None:
        element_schema = ElementSchema()
        # update = element_schema.load(elementDetails, session=db.session).data
        # update.id = element.id

        new_is_end = elementDetails['isEnd']
        if new_is_end and element.isEnd != new_is_end:
            # result = db.engine.execute('select count(id) from elements where parentElementId = {id};'
            # .format(id=element.id))
            # if result.first()['count(id)'] != 0:
            #     abort(404, "Hierarchy is not empty for changing isEnd to True")
            if is_child_exists(elementId):
                abort(404, "Hierarchy is not empty for changing isEnd to True")

        new_name = elementDetails['elementName']
        new_parent_id = elementDetails['parentElementId']
        if element.elementName != new_name:
            if new_parent_id != element.parentElementId:
                data = {}
                result = Element.query.all()
                for i in result:
                    data.update({i.id: [i.elementName, i.parentElementId]})

                # Change branch in chain
                data[elementId][0] = new_name
                data[elementId][1] = new_parent_id
                chain1 = get_all_names(elementId, data)
                chain_values = chain1.values()
                names = []
                for i in chain_values:
                    names.append(i[0])
                set_chain_values = set(names)
                if len(set_chain_values) != len(chain_values):
                    abort(404, "In new hierarchy found name collisions, with change name")
                print("test")
            else:
                if not is_available_name(new_name):
                    abort(404, "ElementName is Incorrect")

                ### It is upward finding
                # result = db.engine.execute('''
                #     WITH RECURSIVE b(parentElementId,id,elementName,isEnd,isIndexed,isRoot) AS
                #     (
                #         SELECT {parentElementId},0,0,0,0,0
                #         UNION ALL
                #         SELECT elements.parentElementId, elements.id,
                #                elements.elementName, elements.isEnd,
                #                elements.isIndexed, elements.isRoot
                #         FROM b, elements
                #         WHERE b.parentElementId = elements.id
                #                    limit 10
                #     ) SELECT * FROM b;
                # '''.format(parentElementId=elementDetails['parentElementId']))
                # hierarchy_array = {}
                # for i in result:
                #     hierarchy_array[i['id']] = [i['elementName'], i['parentElementId']]
                # # Here exist some problem, because checking only from element to upward
                # # Ага, значит такой умный - берешь и запросом всю задачу решаешь, ишь че удумал С:
                #
                # if not is_available_for_insert(new_name, elementId, hierarchy_array):
                #     abort(404, "ElementName already in hierarchy")

                data = {}
                result = Element.query.all()
                for i in result:
                    data.update({i.id: [i.elementName, i.parentElementId]})

                chain1 = get_all_names(elementId, data)
                for i in chain1:
                    if chain1[i][0] == new_name:
                        abort(404, "ElementName already in hierarchy")
        else:
            if new_parent_id != element.parentElementId:
                data = {}
                result = Element.query.all()
                for i in result:
                    data.update({i.id: [i.elementName, i.parentElementId]})

                data[elementId][1] = new_parent_id

                chain1 = get_all_names(elementId, data)
                chain_values = chain1.values()
                names = []
                for i in chain_values:
                    names.append(i[0])
                set_chain_values = set(names)
                if len(set_chain_values) != len(chain_values):
                    abort(404, "In new hierarchy found name collisions")
                print("test")

        update = Element(
            elementName=elementDetails['elementName'],
            isEnd=elementDetails['isEnd'],
            isIndexed=elementDetails['isIndexed'],
            isRoot=elementDetails['isRoot'],
            parentElementId=elementDetails['parentElementId'],
            id=elementId,
        )
        db.session.merge(update)
        db.session.commit()
        data = element_schema.dump(element).data
        return data
    else:
        abort(404, "Element not found for Id: {element_id}".format(element_id=elementId), )


def is_available_name(name):
    if len(name) == 0:
        return False

    for i in name:
        if not is_available_symbol(i):
            return False

    words = name.split(" ")
    for i in words:
        if len(i) == 0:
            return False
    return True


def is_available_symbol(symbol):
    return ('a' <= symbol <= 'z') or \
           ('A' <= symbol <= 'Z') or \
           ('а' <= symbol <= 'я') or \
           ('А' <= symbol <= 'Я') or \
           (symbol == ' ')


def is_available_for_insert(new_name, index, data):
    debug_counter = 0
    current_element = data[index]
    while current_element[1] != -1:
        debug_counter += 1
        if debug_counter > 50:
            return "Overflow"

        new_index = current_element[1]
        if data.get(new_index) is None:
            return "End"

        current_element = data[new_index]
        if current_element[0] == new_name:
            return False
    return True


def is_child_exists(element_id):
    child = Element.query.filter(Element.parentElementId == element_id).count()
    return child != 0


def get_all_names(index, data):
    answer = {}
    upward = get_all_names_upward(index, data)
    for i in upward:
        answer.update({i: upward[i]})

    downward = get_all_names_downward(index, data)
    for i in downward:
        answer.update({i: downward[i]})

    return answer


def get_all_names_upward(index, data):
    if index == -1:
        return {}
    element = data[index]
    names = {index: [element[0], element[1]]}

    for i in data:
        if data[i][1] == element[1]:
            names.update(get_all_names_upward(element[1], data))

    return names


def get_all_names_downward(index, data):
    element = data[index]
    names = {index: [element[0], element[1]]}

    for i in data:
        if data[i][1] == index:
            names.update(get_all_names_downward(i, data))

    return names
