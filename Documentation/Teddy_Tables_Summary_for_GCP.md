User table 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Host | char | 255 |  |  |  |  |
| has\_alias | bit | 1 |  |  | 0 |  |
| name | varchar | 255 | √ |  | null |  |
| email | varchar | 300 |  |  |  |  |
| Update\_priv | enum | 1 |  |  | N |  |
| phone | varchar | 63 | √ |  | null |  |
| password | varchar | 255 | √ |  | null |  |
| Drop\_priv | enum | 1 |  |  | N |  |
| Reload\_priv | enum | 1 |  |  | N |  |
| status | bit | 1 |  |  | 1 |  |
| Process\_priv | enum | 1 |  |  | N |  |
| lastlogin | timestamp | 19 | √ |  | null |  |
| Grant\_priv | enum | 1 |  |  | N |  |
| CDate | timestamp | 19 | √ |  | CURRENT\_TIMESTAMP |  |
| Index\_priv | enum | 1 |  |  | N |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| Show\_db\_priv | enum | 1 |  |  | N |  |
| google\_user\_id | varchar | 255 | √ |  | null |  |
| business\_email | varchar | 300 | √ |  | null |  |
| business\_name | varchar | 255 | √ |  | null |  |
| referral\_code | varchar | 20 | √ |  | null |  |
| referral\_by | int | 10 | √ |  | null |  |
| Repl\_client\_priv | enum | 1 |  |  | N |  |
| Create\_view\_priv | enum | 1 |  |  | N |  |
| nzloyalty\_id | varchar | 255 | √ |  | null |  |
| Create\_routine\_priv | enum | 1 |  |  | N |  |
| Alter\_routine\_priv | enum | 1 |  |  | N |  |
| Create\_user\_priv | enum | 1 |  |  | N |  |
| Event\_priv | enum | 1 |  |  | N |  |
| Trigger\_priv | enum | 1 |  |  | N |  |
| Create\_tablespace\_priv | enum | 1 |  |  | N |  |
| ssl\_type | enum | 9 |  |  |  |  |
| ssl\_cipher | blob | 65535 |  |  |  |  |
| x509\_issuer | blob | 65535 |  |  |  |  |
| x509\_subject | blob | 65535 |  |  |  |  |
| max\_questions | int unsigned | 10 |  |  | 0 |  |
| max\_updates | int unsigned | 10 |  |  | 0 |  |
| max\_connections | int unsigned | 10 |  |  | 0 |  |
| max\_user\_connections | int unsigned | 10 |  |  | 0 |  |
| plugin | char | 64 |  |  | caching\_sha2\_password |  |
| authentication\_string | text | 65535 | √ |  | null |  |
| password\_expired | enum | 1 |  |  | N |  |
| password\_last\_changed | timestamp | 19 | √ |  | null |  |
| password\_lifetime | smallint unsigned | 5 | √ |  | null |  |
| account\_locked | enum | 1 |  |  | N |  |
| Create\_role\_priv | enum | 1 |  |  | N |  |
| Drop\_role\_priv | enum | 1 |  |  | N |  |
| Password\_reuse\_history | smallint unsigned | 5 | √ |  | null |  |
| Password\_reuse\_time | smallint unsigned | 5 | √ |  | null |  |
| Password\_require\_current | enum | 1 | √ |  | null |  |
| User\_attributes | json | 1073741824 | √ |  | null |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id \+ Host \+ User | Primary key | Asc/Asc/Asc |
| email | Must be unique | Asc |
| is\_deleted | Performance | Asc |

## **product**

*This table store **global** information about product in the system*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  | √ |  | PK |
| sku\_id | int | 10 | √ |  | null | FK(sku) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| description\_en | varchar | 4095 |  |  |  |  |
| description\_ar | varchar | 4095 |  |  |  |  |
| nutrition\_en | varchar | 2047 | √ |  | null |  |
| nutrition\_ar | varchar | 2047 | √ |  | null |  |
| subcategory\_id | int | 10 |  |  |  | FK(subcategory) |
| brand\_id | int | 10 |  |  |  | FK(brand) |
| is\_wrappable | bit | 1 |  |  | 1 | 1 \= wrapable, 0 \= not |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| upc | varchar | 31 | √ |  | null |  |
| skucount | int | 10 |  |  | 0 |  |
| origincountry | varchar | 3 | √ |  | null | unused |
| allergicnote\_ar | text | 65535 | √ |  | null | unused |
| allergicnote\_en | text | 65535 | √ |  | null | unused |
| is\_shortdistance | bit | 1 |  |  | 0 | unused |
| is\_customizable | bit | 1 |  |  | 0 |  |
| slug | varchar | 511 | √ |  | null |  |
| howtouse\_ar | text | 65535 | √ |  | null | unused |
| howtouse\_en | text | 65535 | √ |  | null | unused |
| is\_international | bit | 1 |  |  | 0 | unused |
| is\_digital | bit | 1 |  |  | false |  |
| disable\_cash | bit | 1 |  |  | false |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |  |
| brand\_id \+ is\_deleted | Performance | Asc/Asc |  |
| is\_deleted \+ id | Performance | Asc/Asc |  |
| subcategory\_id | Performance | Asc |  |
| subcategory\_id \+ brand\_id | Performance | Asc/Asc |  |
| slug | Must be unique | Asc | This unique column is also nullable |
| upc | Must be unique | Asc | This unique column is also nullable |
| is\_digital | Performance |  |  |

## 

## **sku**

*This table stores the information about SKU (stock keeping unit)*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  | √ |  | PK |
| product\_id | int | 10 |  |  |  | FK(product) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| code | varchar | 127 | √ |  | null | Not used anymore |
| color | varchar | 15 | √ |  | \#000000 |  |
| limit | int | 10 |  |  | 999 | Buy limit for a customer in ordorder |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| item\_number | varchar | 127 | √ |  | null | Internal Dabdoob code |
| upc | varchar | 31 | √ |  | null |  |
| height | decimal | 10,2 | √ |  | null | Not used |
| length | decimal | 10,2 | √ |  | null | Not used |
| weight | decimal | 10,2 | √ |  | null | Not used |
| width | decimal | 10,2 | √ |  | null | Not used |
| box\_count | int | 10 |  |  | 1 | Not used |
| box\_name\_en | varchar | 127 | √ |  | null | Not used |
| box\_name\_ar | varchar | 127 | √ |  | null | Not used |
| ref\_sku\_id | int | 10 | √ |  | null | Parent SKU id (used for assembly child linkage & boxing) |
| assembly\_enabled | bit | 1 | √ |  | null | Assembly feature flag (1 \= base SKU offers assembly; child also marked) |
| assembly\_provider | varchar | 31 | √ |  | null | Assembly fulfillment owner: in-house / third-party / customer |
| allergicnote\_ar | text | 65535 | √ |  | null | Not used |
| allergicnote\_en | text | 65535 | √ |  | null | Not used |
| ingredient\_ar | varchar | 2047 | √ |  | null | Not used |
| ingredient\_en | varchar | 2047 | √ |  | null | Not used |
| slug | varchar | 511 | √ |  | null | Used |
| minorder | int | 10 |  |  | 1 |  |
| unit | varchar | 63 | √ |  | null |  |

| Column(s) | Type | Sort | Anomalies / Notes |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |  |
| code | Must be unique | Asc | This unique column is also nullable |
| is\_deleted \+ id \+ product\_id | Performance | Asc/Asc/Asc |  |
| is\_deleted \+ id \+ ref\_sku\_id | Performance | Asc/Asc/Asc | Used for fast lookup of assembly child SKUs (where ref\_sku\_id points to base) and boxing relationships |
| product\_id \+ id | Performance | Asc/Asc |  |
| slug | Must be unique | Asc | This unique column is also nullable |
| upc | Must be unique | Asc | This unique column is also nullable |

## **brand**

*This table stores brand information **globally** in the system. It can be disabled per country basis via “disabled” table.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  | √ |  | PK |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| information\_en | varchar | 2047 | √ |  | null |  |
| information\_ar | varchar | 2047 | √ |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| displayorder | int | 10 |  |  | 999 |  |
| slug | varchar | 511 | √ |  | null |  |
| origincountry | varchar | 3 | √ |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |  |
| slug | Must be unique | Asc | This unique column is also nullable |

## **category**

*This table stores **global** product category definition for the system. It can be disabled per country basis via “disabled” table.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  | √ |  | PK |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| color | varchar | 15 | √ |  | null |  |
| displayorder | int | 10 |  |  | 999 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| text\_color | varchar | 15 | √ |  | null |  |
| slug | varchar | 511 | √ |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |  |
| slug | Must be unique | Asc | This unique column is also nullable |

## **subcategory**

*This table stores global product subcategory information*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  | √ |  | PK |
| category\_id | int | 10 |  |  |  | FK(category) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| slug | varchar | 511 | √ |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |  |
| category\_id | Performance | Asc |  |
| slug | Must be unique | Asc | This unique column is also nullable |

## **attribute**

*This stores the attribute of products. Right now in the system there are only three attributes: Size, Age, Gender*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  | √ |  | PK |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| appFilterOp | varchar | 31 |  |  |  |  |
| appFilterItemsOp | varchar | 31 |  |  |  |  |
| secondary\_id | int | 10 | √ |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| target | varchar | 31 |  |  | product |  |
| slug | varchar | 511 | √ |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |  |
| is\_deleted | Performance | Asc |  |
| slug | Must be unique | Asc | This unique column is also nullable |

## **attributevalue**

*This table stores the possible values of (product) attribute*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  | √ |  | PK |
| attribute\_id | int | 10 |  |  |  | FK(attribute) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| color | varchar | 15 | √ |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| icon | varchar | 255 | √ |  | null |  |
| slug | varchar | 511 | √ |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |  |
| attribute\_id \+ is\_deleted | Performance | Asc/Asc |  |
| id \+ attribute\_id | Performance | Asc/Asc |  |
| slug | Must be unique | Asc | This unique column is also nullable |

## **product\_attributevalue**

*This table stores product attribute values. Currently there are three attributes (Size, Gender, Age).*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| product\_id | int | 10 |  |  |  |  |
| attributevalue\_id | int | 10 |  |  |  |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| product\_id \+ attributevalue\_id | Primary key | Asc/Asc |

## **invoice**

*This table stores the order that customers made in the front end. The store frontend stores the shopping card separately. When the order is submitted, an invoice is generated.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  | √ |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| device\_id | int | 10 |  |  |  | FK(device) |
| user\_id | int | 10 |  |  |  | FK(user) |
| coupon\_id | int | 10 | √ |  | null | FK(coupon) |
| address\_id | int | 10 |  |  |  | FK(dynamicaddress) |
| paymentmethod\_id | int | 10 |  |  |  | FK(paymentmethod) |
| subtotal | decimal | 10,3 |  |  |  |  |
| discount | decimal | 10,3 |  |  | 0.000 |  |
| delivery | decimal | 10,3 |  |  | 0.000 |  |
| has\_assembly | bit | 1 |  |  | 0 | 1 \= order contains at least one assembly service line |
| pay | decimal | 10,3 |  |  |  | The actual amount that the custthat the customer pays |
| tax | decimal | 10,3 |  |  | 0.000 | VAT value |
| profit | decimal | 10,3 |  |  | 0.000 |  |
| payment\_commission | decimal | 10,3 |  |  | 0.000 |  |
| paymentStatus | tinyint | 3 |  |  | 0 | 1 \= Paid, \-1 \= Expired \=0 \= Not Paid |
| deliveryStatus | bit | 1 |  |  | 0 | 0 \=1 \= delivered, 0 \= else |
| status | tinyint | 3 |  |  | 1 | 1 \= default, \-1 \= cancelled \-2 \= Error When inventoryModel.cancelInvoice(...) is called When inventory.sell(...) fails for any reason When paymentService.createTransaction(...) fails for any reason |
| code | varchar | 63 |  |  |  | Generated from device table |
| parcelJson | json | 1073741824 | √ |  | null | Heavily used |
| routeJson | json | 1073741824 | √ |  | null |  |
| paymentInitJson | json | 1073741824 | √ |  | null | unused |
| paymentResJson | json | 1073741824 | √ |  | null | unused |
| fatoora\_id | int | 10 | √ |  | null | unused |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| EDate | timestamp | 19 |  |  |  | Expired date of this invoice |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| wallet | decimal | 10,3 |  |  | 0.000 |  |
| admin\_id | int | 10 | √ |  | null | FK(admin) \- admin created this invoice |
| adminComment | varchar | 2047 | √ |  | null |  |
| userComment | varchar | 2047 | √ |  | null |  |
| cancelStatus | tinyint | 3 |  |  | 0 | 0 \= nothing, 2 partially cancelled , \= 1 \= fully cancelled |
| applytax | decimal | 10,3 |  |  | 0.000 |  |
| cost | decimal | 10,3 |  |  | 0.000 |  |
| source | varchar | 63 | √ |  | null |  |
| promo\_coupon\_id | varchar | 255 | √ |  | null | Coupon id from promo engine |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| country\_id \+ paymentStatus | Performance | Asc/Asc |
| code | Performance | Asc |
| country\_id \+ id | Performance | Asc/Asc |
| paymentStatus \+ country\_id \+ user\_id | Performance | Asc/Asc/Asc |
| paymentStatus \+ id \+ status | Performance | Asc/Asc/Asc |
| status \+ country\_id \+ id | Performance | Asc/Asc/Asc |
| status \+ paymentStatus \+ EDate | Performance | Asc/Asc/Asc |
| user\_id \+ country\_id \+ status | Performance | Asc/Asc/Asc |

## **invoiceItem**

*This table stores the product item that a customer orders*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  | √ |  | PK |
| invoice\_id | int | 10 |  |  |  | FK(invoice) |
| invoiceParcel\_id | int | 10 |  |  |  | FK(invoiceparcel) |
| inventory\_id | int | 10 |  |  |  | FK(inventory) \- exact row of product sold |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| store\_id | int | 10 |  |  |  | FK(store) |
| price | decimal | 10,3 |  |  |  |  |
| cost | decimal | 10,3 |  |  |  |  |
| sku | json | 1073741824 |  |  |  |  |
| wrapping | json | 1073741824 | √ |  | null |  |
| wrapping\_id | int | 10 | √ |  | null | FK(wrapping) |
| wrapping\_price | decimal | 10,3 |  |  | 0.000 |  |
| cardFrom | varchar | 255 | √ |  | null |  |
| cardTo | varchar | 255 | √ |  | null |  |
| cardMessage | varchar | 1023 | √ |  | null |  |
| restore\_id | int | 10 | √ |  | null | FK(restore) \- wused when performaing order return |
| customtext | text | 65535 | √ |  | null |  |
| old\_price | decimal | 10,3 | √ |  | null |  |
| assembly\_price | decimal | 10,3 | √ |  | null | Assembly service fee (per line when assembly selected) |
| tax | decimal | 10,3 |  |  | 0.000 |  |
| discount | decimal | 10,3 |  |  | 0.000 |  |
| delivery | decimal | 10,3 |  |  | 0.000 |  |
| payment\_commission | decimal | 10,3 |  |  | 0.000 |  |
| vat | decimal | 10,3 |  |  | 0.000 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| inventory\_id | Performance | Asc |
| inventory\_id \+ invoice\_id | Performance | Asc/Asc |
| invoice\_id | Performance | Asc |
| invoiceParcel\_id | Performance | Asc |
| sku\_id \+ store\_id \+ invoice\_id | Performance | Asc/Asc/Asc |

## 

## **hit**

*This is a large table. The data gets flushed on a regular basis.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  | √ |  | PK |
| device\_id | int | 10 | √ |  | null | FK(device) |
| user\_id | int | 10 | √ |  | null | FK(user) |
| target | varchar | 31 |  |  |  | product |
| target\_id | int | 10 |  |  |  |  |
| time | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| target \+ device\_id \+ time | Performance | Asc/Asc/Desc |
| target \+ user\_id \+ time | Performance | Asc/Asc/Desc |
| time | Performance | Desc |

## **productfavorite**

*Unused. This table stores customers’ favorited product information. API is ready but not implemented in client.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  | √ |  | PK |
| product\_id | int | 10 |  |  |  | FK(product) |
| user\_id | int | 10 |  |  |  | FK(user) |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| product\_id \+ user\_id | Must be unique | Asc/Asc |

## **inventory**

*This table stores 1 : 1 correlation with actual product items. So if there are 1000 teddy bears, there will be 1000 entries in this table.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  | √ |  | PK |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| cost | decimal | 10,3 |  |  | 0.000 |  |
| document\_id | int | 10 |  |  |  | FK(inventorydocument)f |
| sold | varchar | 15 | √ |  | null | Invoice, document (if null, product on the shelf) |
| sold\_id | int | 10 | √ |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| expiry\_date | datetime | 23 | √ |  | null |  |
| vat | decimal | 10,3 |  |  | 0.000 |  |
| vatperc | decimal | 10,2 |  |  | 0.00 |  |

| *Column(s)* | *Type* | *Sort* |
| ----- | ----- | ----- |
| *id* | *Primary key* | *Asc* |
| *CDate* | *Performance* | *Asc* |
| *document\_id \+ sku\_id* | *Performance* | *Asc/Asc* |
| *sku\_id \+ expiry\_date \+ sold \+ cost \+ id* | *Performance* | *Asc/Asc/Asc/Asc/Asc* |
| *sku\_id \+ sold \+ CDate* | *Performance* | *Asc/Asc/Asc* |
| *sku\_id \+ sold \+ document\_id \+ CDate* | *Performance* | *Asc/Asc/Asc/Asc* |
| *sku\_id \+ sold \+ document\_id \+ sold\_id* | *Performance* | *Asc/Asc/Asc/Asc* |
| *sold \+ document\_id \+ sku\_id \+ expiry\_date* | *Performance* | *Asc/Asc/Asc/Asc* |
| *sold \+ expiry\_date* | *Performance* | *Asc/Asc* |
| *sold\_id \+ sku\_id* | *Performance* | *Asc/Asc* |
| *sold \+ sku\_id \+ document\_id* | *Performance* | *Asc/Asc/Asc* |
| *sold \+ sku\_id \+ expiry\_date* | *Performance* | *Asc/Asc/Asc* |
| *sold\_id \+ sold* | *Performance* | *Asc/Asc* |

