## cc\_product\_view

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  |  |  |
| slug | varchar(511) | 511 | √ |  |  |  |
| country\_id | int | 10 |  |  | 0 |  |
| sku\_id | int | 10 | √ |  |  |  |
| name\_en | varchar(255) | 255 |  |  |  |  |
| name\_ar | varchar(255) | 255 |  |  |  |  |
| description\_en | varchar(4095) | 4095 |  |  |  |  |
| description\_ar | varchar(4095) | 4095 |  |  |  |  |
| nutrition\_en | varchar(2047) | 2047 | √ |  |  |  |
| nutrition\_ar | varchar(2047) | 2047 | √ |  |  |  |
| allergicnote\_en | text |  | √ |  |  |  |
| allergicnote\_ar | text |  | √ |  |  |  |
| howtouse\_en | text |  | √ |  |  |  |
| howtouse\_ar | text |  | √ |  |  |  |
| upc | varchar(31) | 3 | √ |  |  |  |
| subcategory\_id | int | 10 |  |  |  |  |
| brand\_id | int | 10 |  |  |  |  |
| is\_wrappable | tinyint(1) | 1 |  |  | 1 |  |
| is\_shortdistance | tinyint(1) | 1 |  |  | 0 |  |
| is\_international | tinyint(1) | 1 |  |  | 0 |  |
| is\_customizable | tinyint(1) | 1 |  |  | 0 |  |
| is\_deleted | tinyint(1) | 1 |  |  | 0 |  |
| is\_disabled | bigint |  |  |  | 0 |  |
| CDate | timestamp |  |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime(3) |  |  |  | CURRENT\_TIMESTAMP(3) |  |
| sku\_slug | varchar(511) | 511 | √ |  |  |  |
| sku\_name\_en | varchar(255) | 255 | √ |  |  |  |
| sku\_name\_ar | varchar(255) | 255 | √ |  |  |  |
| sku\_price | decimal(10,3) |  | √ |  |  |  |
| sku\_old\_price | decimal(10,3) |  | √ |  |  |  |
| sku\_code | varchar(127) | 127 | √ |  |  |  |
| sku\_item\_number | varchar(127) | 127 | √ |  |  |  |
| sku\_upc | varchar(31) | 31 | √ |  |  |  |
| sku\_limit | int | 10 | √ |  | 999 |  |
| sku\_color | varchar(15) | 15 | √ |  | \#000000 |  |
| sku\_width | decimal(10,2) |  | √ |  |  |  |
| sku\_height | decimal(10,2) |  | √ |  |  |  |
| sku\_length | decimal(10,2) |  | √ |  |  |  |
| sku\_weight | decimal(10,2) |  | √ |  |  |  |
| sku\_ingredient\_en | varchar(2047) | 2047 | √ |  |  |  |
| sku\_ingredient\_ar | varchar(2047) | 2047 | √ |  |  |  |
| sku\_allergicnote\_en | text |  | √ |  |  |  |
| sku\_allergicnote\_ar | text |  | √ |  |  |  |
| sku\_is\_deleted | tinyint(1) |  | √ |  | 0 |  |
| sku\_unit | varchar(63) | 63 | √ |  |  |  |
| sku\_minorder | int | 10 | √ |  | 1 |  |
| sku\_is\_disabled | bigint |  |  |  | 0 |  |
| sku\_CDate | timestamp |  | √ |  | CURRENT\_TIMESTAMP |  |
| sku\_UDate | datetime(3) |  | √ |  | CURRENT\_TIMESTAMP(3) |  |
| subcategory\_category\_id | int | 10 | √ |  |  |  |
| subcategory\_slug | varchar(511) | 511 | √ |  |  |  |
| subcategory\_name\_en | varchar(255) | 255 | √ |  |  |  |
| subcategory\_name\_ar | varchar(255) | 255 | √ |  |  |  |
| subcategory\_is\_disabled | int | 10 | √ |  | 0 |  |
| subcategory\_is\_deleted | int | 10 |  |  | 0 |  |
| subcategory\_CDate | timestamp |  | √ |  |  |  |
| subcategory\_UDate | datetime(3) |  | √ |  |  |  |
| brand\_slug | varchar(511) |  | √ |  |  |  |
| brand\_name\_en | varchar(255) |  | √ |  |  |  |
| brand\_name\_ar | varchar(255) |  | √ |  |  |  |
| brand\_is\_disabled | int |  | √ |  | 0 |  |
| brand\_is\_deleted | int |  |  |  | 0 |  |
| brand\_CDate | timestamp |  | √ |  |  |  |
| brand\_UDate | datetime(3) |  | √ |  |  |  |
| brand\_origincountry | varchar(3) |  | √ |  |  |  |
| category\_id | int |  | √ |  | 0 |  |
| category\_slug | varchar(511) |  | √ |  |  |  |
| category\_name\_en | varchar(255) |  | √ |  |  |  |
| category\_name\_ar | varchar(255) |  | √ |  |  |  |
| category\_color | varchar(15) |  | √ |  |  |  |
| category\_is\_disabled | int |  | √ |  | 0 |  |
| category\_is\_deleted | int |  |  |  | 0 |  |
| category\_CDate | timestamp |  | √ |  |  |  |
| category\_UDate | datetime(3) |  | √ |  |  |  |
| all\_disabled | bigint |  | √ |  |  |  |
| available | decimal(23,0) |  |  |  | 0 |  |
| sold | bigint |  |  |  | 0 |  |
| sku\_count | int |  |  |  | 0 |  |
| origincountry | varchar(3) |  | √ |  |  |  |

## 

## cc\_sku\_view

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  |  |  |
| slug | varchar(511) | 511 | √ |  |  |  |
| country\_id | int | 10 |  |  | 0 |  |
| name\_en | varchar(255) | 255 |  |  |  |  |
| name\_ar | varchar(255) | 255 |  |  |  |  |
| price | decimal(10,3) |  | √ |  |  |  |
| old\_price | decimal(10,3) |  | √ |  |  |  |
| score | int | 10 | √ |  | 100 |  |
| code | varchar(127) | 127 | √ |  |  |  |
| item\_number | varchar(127) | 127 | √ |  |  |  |
| upc | varchar(31) | 31 | √ |  |  |  |
| limit | int | 10 |  |  | 999 |  |
| color | varchar(15) | 15 | √ |  | \#000000 |  |
| width | decimal(10,2) |  | √ |  |  |  |
| height | decimal(10,2) |  | √ |  |  |  |
| length | decimal(10,2) |  | √ |  |  |  |
| weight | decimal(10,2) |  | √ |  |  |  |
| box\_name\_en | varchar(127) | 127 | √ |  |  |  |
| box\_name\_ar | varchar(127) | 127 | √ |  |  |  |
| box\_count | int | 10 |  |  | 1 |  |
| ref\_sku\_id | int | 10 | √ |  |  |  |
| ingredient\_en | varchar(2047) | 2047 | √ |  |  |  |
| ingredient\_ar | varchar(2047) | 2047 | √ |  |  |  |
| allergicnote\_en | text |  | √ |  |  |  |
| allergicnote\_ar | text |  | √ |  |  |  |
| is\_deleted | tinyint(1) | 1 |  |  | 0 |  |
| unit | varchar(63) | 63 | √ |  |  |  |
| minorder | int | 10 |  |  | 1 |  |
| is\_disabled | bigint |  |  |  | 0 |  |
| CDate | timestamp |  |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime(3) |  |  |  | CURRENT\_TIMESTAMP(3) |  |
| product\_id | int | 10 | √ |  | 0 |  |
| product\_slug | varchar(511) | 511 | √ |  |  |  |
| product\_sku\_id | int | 10 | √ |  |  |  |
| product\_name\_en | varchar(255) | 255 | √ |  |  |  |
| product\_name\_ar | varchar(255) | 255 | √ |  |  |  |
| product\_description\_en | varchar(4095) | 4095 | √ |  |  |  |
| product\_description\_ar | varchar(4095) | 4095 | √ |  |  |  |
| product\_nutrition\_en | varchar(2047) | 2047 | √ |  |  |  |
| product\_nutrition\_ar | varchar(2047) | 2047 | √ |  |  |  |
| product\_allergicnote\_en | text |  | √ |  |  |  |
| product\_allergicnote\_ar | text |  | √ |  |  |  |
| product\_howtouse\_en | text |  | √ |  |  |  |
| product\_howtouse\_ar | text |  | √ |  |  |  |
| product\_upc | varchar(31) | 31 | √ |  |  |  |
| product\_subcategory\_id | int | 10 | √ |  |  |  |
| product\_brand\_id | int | 10 | √ |  |  |  |
| product\_is\_wrappable | tinyint(1) | 1 | √ |  | 1 |  |
| product\_is\_shortdistance | tinyint(1) | 1 | √ |  | 0 |  |
| product\_is\_international | tinyint(1) | 1 | √ |  | 0 |  |
| product\_is\_customizable | tinyint(1) | 1 | √ |  | 0 |  |
| product\_is\_deleted | tinyint(1) | 1 | √ |  | 0 |  |
| product\_is\_disabled | bigint |  |  |  | 0 |  |
| product\_CDate | timestamp |  | √ |  | CURRENT\_TIMESTAMP |  |
| product\_UDate | datetime(3) |  | √ |  | CURRENT\_TIMESTAMP(3) |  |
| subcategory\_category\_id | int | 10 | √ |  |  |  |
| subcategory\_slug | varchar(511) | 511 | √ |  |  |  |
| subcategory\_name\_en | varchar(255) | 255 | √ |  |  |  |
| subcategory\_name\_ar | varchar(255) | 255 | √ |  |  |  |
| subcategory\_is\_disabled | int | 10 | √ |  |  |  |
| subcategory\_CDate | timestamp |  | √ |  |  |  |
| subcategory\_UDate | datetime(3) |  | √ |  |  |  |
| subcategory\_is\_deleted | int | 10 |  |  | 0 |  |
| brand\_slug | varchar(511) | 511 | √ |  |  |  |
| brand\_name\_en | varchar(255) | 255 | √ |  |  |  |
| brand\_name\_ar | varchar(255) | 255 | √ |  |  |  |
| brand\_is\_disabled | int | 10 | √ |  | 0 |  |
| brand\_CDate | timestamp |  | √ |  |  |  |
| brand\_UDate | datetime(3) |  | √ |  |  |  |
| brand\_is\_deleted | int | 10 |  |  |  |  |
| brand\_origincountry | varchar(3) | 3 | √ |  |  |  |
| category\_id | int | 10 | √ |  | 0 |  |
| category\_slug | varchar(511) | 511 | √ |  |  |  |
| category\_name\_en | varchar(255) | 255 | √ |  |  |  |
| category\_name\_ar | varchar(255) | 255 | √ |  |  |  |
| category\_is\_disabled | int | 10 | √ |  |  |  |
| category\_CDate | timestamp |  | √ |  |  |  |
| category\_UDate | datetime(3) |  | √ |  |  |  |
| category\_is\_deleted | int | 10 |  |  | 0 |  |
| all\_disabled | bigint |  | √ |  |  |  |
| available | decimal(23,0) |  |  |  | 0 |  |
| sold | bigint |  |  |  | 0 |  |
| product\_origincountry | varchar(3) | 3 | √ |  |  |  |

## 

## cc\_brand\_view

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  |  |  |
| slug | varchar(511) | 511 | √ |  |  |  |
| name\_en | varchar(255) | 255 |  |  |  |  |
| name\_ar | varchar(255) | 255 |  |  |  |  |
| CDate | timestamp |  |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime(3) |  |  |  | CURRENT\_TIMESTAMP(3) |  |
| origincountry | varchar(3) | 3 | √ |  |  |  |
| displayorder | int | 10 |  |  | 999 |  |
| is\_disabled | bigint |  |  |  | 0 |  |
| country\_id | int | 10 |  |  | 0 |  |

## 

## cc\_category\_sorted\_view

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  |  |  |
| slug | varchar(511) | 511 | √ |  |  |  |
| name\_en | varchar(255) | 255 |  |  |  |  |
| name\_ar | varchar(255) | 255 |  |  |  |  |
| color | varchar(15) | 15 | √ |  |  |  |
| text\_color | varchar(15) | 15 | √ |  |  |  |
| displayorder | bigint |  |  |  | 0 |  |
| CDate | timestamp |  |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime(3) |  |  |  | CURRENT\_TIMESTAMP(3) |  |
| is\_disabled | bigint |  |  |  | 0 |  |
| country\_id | int | 10 |  |  | 0 |  |

## 

## cc\_category\_view

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  |  |  |
| slug | varchar(511) | 511 | √ |  |  |  |
| name\_en | varchar(255) | 255 |  |  |  |  |
| name\_ar | varchar(255) | 255 |  |  |  |  |
| color | varchar(15) | 15 | √ |  |  |  |
| text\_color | varchar(15) | 15 | √ |  |  |  |
| displayorder | int | 10 |  |  | 999 |  |
| CDate | timestamp |  |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime(3) |  |  |  | CURRENT\_TIMESTAMP(3) |  |
| is\_disabled | bigint |  |  |  | 0 |  |
| country\_id | int | 10 |  |  | 0 |  |

## 

## invoice\_view

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  |  |  |
| country\_id | int | 10 |  |  |  |  |
| device\_id | int | 10 |  |  |  |  |
| user\_id | int | 10 |  |  |  |  |
| admin\_id | int | 10 | √ |  |  |  |
| coupon\_id | int | 10 | √ |  |  |  |
| address\_id | int | 10 |  |  |  |  |
| paymentmethod\_id | int | 10 |  |  |  |  |
| subtotal | decimal(10,3) |  |  |  |  |  |
| discount | decimal(10,3) |  |  |  | 0.000 |  |
| delivery | decimal(10,3) |  |  |  | 0.000 |  |
| pay | decimal(10,3) |  |  |  |  |  |
| wallet | decimal(10,3) |  |  |  | 0.000 |  |
| profit | decimal(10,3) |  |  |  | 0.000 |  |
| payment\_commission | decimal(10,3) |  |  |  | 0.000 |  |
| paymentStatus | tinyint | 1 |  |  | 0 |  |
| deliveryStatus | tinyint(1) | 1 |  |  | 0 |  |
| cancelStatus | tinyint | 1 |  |  | 0 |  |
| status | tinyint | 1 |  |  | 1 |  |
| code | varchar(63) | 63 |  |  |  |  |
| CDate | timestamp |  |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime(3) |  |  |  | CURRENT\_TIMESTAMP(3) |  |
| applytax | decimal(10,3) |  |  |  | 0.000 |  |
| name | varchar(255) | 255 | √ |  |  |  |
| email | varchar(300) | 300 | √ |  |  |  |
| phone | varchar(63) | 63 | √ |  |  |  |
| address\_phone | varchar(255) | 255 | √ |  |  |  |
| coupon\_code | varchar(63) | 63 | √ |  |  |  |
| coupon\_type | varchar(7) | 7 | √ |  |  |  |
| coupon\_amount | decimal(10,3) |  | √ |  |  |  |
| coupon\_coupongroup\_id | int | 10 | √ |  | 0 |  |
| paymentmethod\_name | varchar(255) | 255 | √ |  |  |  |
| parcel\_count | bigint |  |  |  | 0 |  |

## 

## parcel\_view

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  |  |  |
| invoice\_id | int | 10 |  |  |  |  |
| store\_id | int | 10 |  |  |  |  |
| delivery\_date | date |  |  |  |  |  |
| delivery\_cost | decimal(10,3) |  |  |  |  |  |
| subtotal | decimal(10,3) |  |  |  | 0.000 |  |
| discount | decimal(10,3) |  |  |  | 0.000 |  |
| wallet | decimal(10,3) |  |  |  | 0.000 |  |
| pay | decimal(10,3) |  |  |  | 0.000 |  |
| tax | decimal(10,3) |  |  |  | 0.000 |  |
| profit | decimal(10,3) |  |  |  | 0.000 |  |
| delivery | decimal(10,3) |  |  |  | 0.000 |  |
| status | int | 10 |  |  | 0 |  |
| CDate | timestamp |  |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime(3) |  |  |  | CURRENT\_TIMESTAMP(3) |  |
| item\_count | bigint |  |  |  | 0 |  |
| invoice\_paymentStatus | tinyint | 1 | √ |  | 0 |  |
| country\_id | int | 10 | √ |  |  |  |
| invoice\_status | tinyint | 1 | √ |  | 1 |  |
| address\_id | int | 1 | √ |  |  |  |

## 

