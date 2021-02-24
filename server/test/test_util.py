from ..src.Util import parseResearch, parseResearchBack, parseAllResearch, parseAllResearchBack
import unittest


class Test_parser(unittest.TestCase):
    def test_parseResearch(self):
        rdsResponse = [
            {
                "portIn": [
                    {
                        "port": "port-reva",
                        "properties": [
                            {
                                "portType": "fileStorage",
                                "value": "True"
                            },
                            {
                                "portType": "customProperties",
                                "value": [
                                    {
                                        "key": "filepath",
                                        "value": "/RDSTest"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "portOut": [
                    {
                        "port": "port-zenodo",
                        "properties": [
                            {
                                "portType": "metadata",
                                "value": "True"
                            },
                            {
                                "portType": "customProperties",
                                "value": [
                                    {
                                        "key": "projectId",
                                        "value": "719218"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "researchId": 0,
                "researchIndex": 0,
                "status": 1,
                "userId": "admin"
            },
            {
                "portIn": [
                    {
                        "port": "port-owncloud",
                        "properties": [
                            {
                                "portType": "fileStorage",
                                "value": "True"
                            },
                            {
                                "portType": "customProperties",
                                "value": [
                                    {
                                        "key": "filepath",
                                        "value": "/rocratetestfolder"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "portOut": [
                    {
                        "port": "port-datasafe",
                        "properties": [
                            {
                                "portType": "metadata",
                                "value": "True"
                            }
                        ]
                    }
                ],
                "researchId": 1,
                "researchIndex": 1,
                "status": 1,
                "userId": "admin"
            },
            {
                "portIn": [
                    {
                        "port": "port-reva",
                        "properties": [
                            {
                                "portType": "fileStorage",
                                "value": "True"
                            },
                            {
                                "portType": "customProperties",
                                "value": [
                                    {
                                        "key": "filepath",
                                        "value": "/RDSTest"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "portOut": [
                    {
                        "port": "port-zenodo",
                        "properties": [
                            {
                                "portType": "metadata",
                                "value": "True"
                            },
                            {
                                "portType": "customProperties",
                                "value": [
                                    {
                                        "key": "projectId",
                                        "value": "719218"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "researchId": 2,
                "researchIndex": 2,
                "status": 1,
                "userId": "admin"
            }
        ]

        self.assertEqual(rdsResponse[0], parseResearchBack(
            parseResearch(rdsResponse[0])))
        self.assertEqual(rdsResponse, parseAllResearchBack(
            parseAllResearch(rdsResponse)))
