from unittest.mock import patch
import pytest
from strompris_api import get_access_token, get_products

@patch('strompris_api.requests.post')
def test_get_access_token(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'accessToken': 'test_token'}

    token = get_access_token('valid_client_id', 'valid_client_secret')

    assert token == 'test_token'

    with pytest.raises(ValueError):
        get_access_token('', '')


@patch('strompris_api.get_access_token')
@patch('strompris_api.requests.get')
def test_get_products(mock_get, mock_get_access_token):
    response_data = [
        {
            "id": 10005,
            "name": "Istad Kraft AS",
            "organizationNumber": 923253920,
            "pricelistUrl": "https://www.istadkraft.no/prisliste-istad-kraft-privat",
            "products": [
                {
                    "id": 21226,
                    "productId": 10084,
                    "name": "Istad Spot",
                    "agreementTime": 0,
                    "agreementTimeUnit": "year",
                    "billingFrequency": 1,
                    "billingFrequencyUnit": "month",
                    "addonPriceMinimumFixedFor": 1,
                    "addonPriceMinimumFixedForUnit": "month",
                    "productType": "hourly_spot",
                    "paymentType": "after",
                    "monthlyFee": 49,
                    "addonPrice": 0.0799,
                    "elCertificatePrice": 0.05215,
                    "maxKwhPerYear": 0,
                    "feeMandatoryType": "none",
                    "feePostalLetter": 39,
                    "feePostalLetterApplied": True,
                    "otherConditions": "",
                    "orderUrl": "https://www.istadkraft.no/produkter/istad-spot",
                    "applicableToCustomerType": "allCustomers",
                    "standardAlert": None,
                    "cabinProduct": False,
                    "priceChangedAt": "2022-10-31T07:00:08.000Z",
                    "purchaseAddonPrice": 0,
                    "expiredAt": None,
                    "createdAt": "2024-04-18T07:00:00.000Z",
                    "updatedAt": "2024-04-18T07:00:00.000Z",
                    "deletedAt": None,
                    "salesNetworks": [
                        {
                            "id": "NO",
                            "type": "country",
                            "name": "Norge",
                            "kwPrice": 0,
                            "purchaseKwPrice": 0
                        }
                    ],
                    "associations": [
                        {
                            "id": 54,
                            "name": "Huseiernes Landsforbund",
                            "isCommon": True
                        }
                    ],
                    "vatExemption": False
                },
            ]
        },
    ]

    mock_get_access_token.return_value = 'test_token'
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = response_data

    products = get_products('2023-01-01')
    assert len(products) == len(response_data)

    for product, expected in zip(products, response_data):
        assert product.id == expected["id"]
        assert product.name == expected["name"]
        assert product.organizationNumber == expected["organizationNumber"]
        assert product.pricelistUrl == expected["pricelistUrl"]

        assert len(product.products) == len(expected["products"])
        for prod, exp_prod in zip(product.products, expected["products"]):
            assert prod.id == exp_prod["id"]
            assert prod.productId == exp_prod["productId"]
            assert prod.name == exp_prod["name"]

            assert len(prod.salesNetworks) == len(exp_prod["salesNetworks"])
            for sn, exp_sn in zip(prod.salesNetworks, exp_prod["salesNetworks"]):
                assert sn.id == exp_sn["id"]
                assert sn.type == exp_sn["type"]

            assert len(prod.salesNetworks) == len(exp_prod["salesNetworks"])
            for sn, exp_sn in zip(prod.salesNetworks, exp_prod["salesNetworks"]):
                assert sn.id == exp_sn["id"]
                assert sn.type == exp_sn["type"]

            assert len(prod.associations) == len(exp_prod["associations"])
            for association, exp_association in zip(prod.associations, exp_prod["associations"]):
                assert association.id == exp_association["id"]
                assert association.name == exp_association["name"]


    with pytest.raises(ValueError):
        get_products('01-01-2023')