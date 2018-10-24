# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from classifier.models.create_element import CreateElement  # noqa: E501
from classifier.models.element_details import ElementDetails  # noqa: E501
from classifier.models.update_element_details import UpdateElementDetails  # noqa: E501
from classifier.test import BaseTestCase


class TestAnyController(BaseTestCase):
    """AnyController integration test stubs"""

    def test_create_element(self):
        """Test case for create_element

        
        """
        createElement = CreateElement()
        response = self.client.open(
            '/api/element',
            method='POST',
            data=json.dumps(createElement),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_element(self):
        """Test case for delete_element

        
        """
        response = self.client.open(
            '/api/element/{elementId}'.format(elementId=56),
            method='DELETE',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_element(self):
        """Test case for get_element

        
        """
        response = self.client.open(
            '/api/element/{elementId}'.format(elementId=56),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_elements(self):
        """Test case for list_elements

        
        """
        response = self.client.open(
            '/api/elements',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_element(self):
        """Test case for update_element

        
        """
        elementDetails = UpdateElementDetails()
        response = self.client.open(
            '/api/element/{elementId}'.format(elementId=56),
            method='PUT',
            data=json.dumps(elementDetails),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
