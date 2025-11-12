## ![][image1] 

# Dabdoob Database Schema

[**Tables	5**](#tables)

[**\_logf	5**](#_log)

[acknowledge	7](#acknowledge)

[activity	8](#activity)

[address	12](#address)

[addressfield	13](#addressfield)

[addresstype	15](#addresstype)

[addressvalidation	16](#addressvalidation)

[admin	18](#admin)

[admin\_home	19](#admin_home)

[admin\_target	20](#admin_target)

[area	20](#area)

[asset	22](#asset)

[attribute	23](#attribute)

[attributevalue	25](#attributevalue)

[badge ☠️	26](#badge-☠️)

[banner	28](#banner)

[brand	29](#brand)

[buyxgety ☠️	30](#buyxgety-☠️)

[buyxgety\_item ☠️	32](#buyxgety_item-☠️)

[cashflow	32](#cashflow)

[cashflow\_item	34](#cashflow_item)

[category	35](#category)

[collection	36](#collection)

[collection\_filter	38](#collection_filter)

[collection\_product	39](#collection_product)

[columnconfig	40](#columnconfig)

[country	43](#country)

[coupon	47](#coupon)

[coupon\_user	50](#coupon_user)

[couponsku	51](#couponsku)

[credentials	52](#credentials)

[creditnote	53](#creditnote)

[deliverymethod ☠️	55](#deliverymethod-☠️)

[deliverymethod\_area ☠️	57](#deliverymethod_area-☠️)

[deposit	58](#deposit)

[device	60](#device)

[digital\_gift	63](#digital_gift)

[disabled	65](#disabled)

[donations	66](#donations)

[dynamicaddress	66](#dynamicaddress)

[entity\_icon ☠️	68](#entity_icon-☠️)

[entitystatus ☠️	69](#entitystatus-☠️)

[exchange ☠️	70](#exchange-☠️)

[faq ☠️	71](#faq-☠️)

[featureannouncement	72](#featureannouncement)

[featureannouncement\_admin	73](#featureannouncement_admin)

[featuredcollection ☠️	74](#featuredcollection-☠️)

[giftcard	75](#giftcard)

[giftcardoption	77](#giftcardoption)

[hit	78](#hit)

[home	79](#home)

[homepage	81](#homepage)

[icon☠️	82](#icon☠️)

[identity☠️	84](#identity☠️)

[inventory	85](#inventory)

[inventorydocument	87](#inventorydocument)

[inventorydraft	90](#inventorydraft)

[invoice	92](#invoice)

[invoiceItem	96](#invoiceitem)

[invoiceparcel (not used)	99](#invoiceparcel-\(not-used\))

[invoiceparcel\_admin	101](#invoiceparcel_admin)

[itemorder\_country	103](#itemorder_country)

[justintimeagreement	104](#justintimeagreement)

[landing☠️	105](#landing☠️)

[legacyusers☠️	107](#legacyusers☠️)

[main\_banner	109](#main_banner)

[media	110](#media)

[notify	112](#notify)

[notify\_offers	113](#notify_offers)

[nubox ☠️	115](#nubox-☠️)

[outlet ☠️	116](#outlet-☠️)

[paymentmethod	118](#paymentmethod)

[permission	120](#permission)

[pricecampaign ☠️	121](#pricecampaign-☠️)

[pricecampaign\_sku ☠️	122](#pricecampaign_sku-☠️)

[pricehistory	123](#pricehistory)

[pricing ☠️	124](#pricing-☠️)

[product	125](#product)

[product\_attributevalue	128](#product_attributevalue)

[product\_badge	129](#product_badge)

[productfavorite	130](#productfavorite)

[relatedproduct ☠️	130](#relatedproduct-☠️)

[relatedtableconfig	131](#relatedtableconfig)

[resetHash	133](#resethash)

[restore	134](#restore)

[restoreitem	136](#restoreitem)

[role	137](#role)

[search ☠️	138](#search-☠️)

[setting	139](#setting)

[short\_deep\_url	140](#short_deep_url)

[shortcut ☠️	141](#shortcut-☠️)

[sku	143](#sku)

[sku\_attributevalue ☠️	146](#sku_attributevalue-☠️)

[sku\_country	146](#sku_country)

[sku\_suggestiongroup	148](#sku_suggestiongroup)

[slider	148](#slider)

[smsprovider	150](#smsprovider)

[smsprovider\_log	151](#smsprovider_log)

[snapshot\_inventory	152](#snapshot_inventory)

[staticpage	155](#staticpage)

[statushistory	156](#statushistory)

[store	157](#store)

[store\_area	159](#store_area)

[store\_wrapping	161](#store_wrapping)

[subcategory	162](#subcategory)

[suggestiongroup	163](#suggestiongroup)

[suggestiongroup\_sku	164](#suggestiongroup_sku)

[supplier	165](#supplier)

[supplier\_sku	166](#supplier_sku)

[suppliercontact	167](#suppliercontact)

[tag	169](#tag)

[tag\_product	170](#tag_product)

[tag\_product\_pending	170](#tag_product_pending)

[taxgroup	172](#taxgroup)

[taxgroup\_item	173](#taxgroup_item)

[timeslot ☠️	173](#timeslot-☠️)

[tmp\_badge\_migrate	175](#tmp_badge_migrate)

[transaction	176](#transaction)

[user	178](#user)

[userList ☠️	183](#userlist-☠️)

[userMarklist	184](#usermarklist)

[userMarklist\_target	186](#usermarklist_target)

[wallettransaction	186](#wallettransaction)

[websiteMenuItem ☠️	188](#websitemenuitem-☠️)

[Widget	190](#widget)

[wrapping	191](#wrapping)

[wrapping\_country	192](#wrapping_country)

# 

# **Tables** {#tables}

## \_log {#_log}

*Ack PO*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| user\_id | int | 10 |  √ |  |  |  |
| device\_id | int | 10 | √ |  |  |  |
| method | varchar | 15 |  |  |  |  |
| path | varchar | 2048 |  |  |  |  |
| ip | varchar | 46 |  |  |  |  |
| token | varchar | 1023 | √ |  |  |  |
| browser | varchar | 2048 |  |  |  |  |
| body | longtext | 2147483647 | √ |  |  |  |
| headers | json | 1073741824 | √ |  |  |  |
| responseCode | int | 10 |  |  |  |  |
| responseTime | float | 12 |  |  |  |  |
| time | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| admin\_id | int | 10 | √ |  |  |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| device\_id | Performance | Asc |
| device\_id \+ time | Performance | Asc |
| time | Performance | Asc |
| user\_id | Performance | Asc |
| user\_id \+ time | Performance | Asc |

## acknowledge {#acknowledge}

*Ack PO ?*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| target | varchar | 45 |  |  |  | “inventory\_document” |
| target\_id | int | 10 |  |  |  |  |
| country\_id | int | 10 |  √  |  | null | FK(country) |
| action | varchar | 100 |  |  | ack | No other value at the moment |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

## activity {#activity}

*This table stores all the recorded activities deemed important* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| action | varchar | 31 |  |  |  |  |
| target | varchar | 31 |  √  |  | null | address addressfield addresstype addressvalidation admin area area-geo attribute attributevalue banner brand cashflow category collection contcat controlcenter country country-area country-governorate coupon coupongroup creditnote dashboard deliverymethod debitnote debug debug-latestdevice deposit document driver-app dynamicaddress failed featureAnnouncement giftcard giftcardoption governorate home homepage homepage-order inventory justintimeAgreement media media-reorder normal offer one-tap onlineflow order parcel paymentmethod paymentmethod-default paymentmethod-enable paymentmethod-hide paymentmethod-order product reset restore role settings settings-referral settings-verification sku slider smsprovider smsprovider-enable smsprovider-order staticpage store store-area store-governorate subcategory suggestionGroup supplier supplier-contact tag taxGroup transporter user video widget wrapping |
| target\_id | int | 10 |  √  |  | null |  |
| country\_id | int | 10 |  √  |  | null | FK(country\_id) |
| body | json | 1073741824 |  √  |  | null | Changes rom |
| raw | json | 1073741824 |  √  |  | null | Raw from frontend |
| time | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| target \+ action \+ admin\_id \+ country\_id \+ target\_id \+ id | Performance | Asc/Asc/Asc/Asc/Asc/Desc |
| target\_id \+ action \+ country\_id \+ target \+ time | Performance | Asc/Asc/Asc/Asc/Asc |
| admin\_id | Performance | Asc |
| admin\_id \+ action | Performance | Asc/Asc |
| admin\_id \+ time | Performance | Asc/Asc |
| time | Performance | Asc |

## address {#address}

*Unused. Check dynamic address table.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  |  |
| user\_id | int | 10 |  |  |  |  |
| area\_id | int | 10 |  |  |  |  |
| name | varchar | 255 |  |  |  |  |
| avenue | varchar | 255 |  √  |  | null |  |
| street | varchar | 255 |  √  |  | null |  |
| building | varchar | 255 |  √  |  | null |  |
| floor | varchar | 255 |  √  |  | null |  |
| apartment | int | 10 |  √  |  | null |  |
| info | varchar | 1023 |  √  |  | null |  |
| phone | varchar | 31 |  √  |  | null |  |
| landline | varchar | 31 |  √  |  | null |  |
| lat | double | 22 |  √  |  | null |  |
| lng | double | 22 |  √  |  | null |  |
| address\_id | int | 10 |  √  |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| user\_id | Performance | Asc |

## addressfield {#addressfield}

*This table is used to construct address form (?)*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| addresstype\_id | int | 10 |  |  |  | FK(addresstype) |
| row | int | 10 |  |  |  |  |
| key | varchar | 255 |  |  |  |  |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| type | varchar | 255 |  |  |  |  |
| reset | varchar | 255 |  √  |  | null |  |
| depend | varchar | 255 |  √  |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| displayorder | int | 10 |  |  | 0 |  |
| options | json | 1073741824 |  √  |  | null |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| addresstype\_id | Performance | Asc |

## addresstype {#addresstype}

*This table is used to construct address form (?)*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| fill\_street | varchar | 255 |  √  |  | null |  |
| template\_en | varchar | 255 |  |  |  |  |
| template\_ar | varchar | 255 |  √  |  | null |  |
| is\_active | bit | 1 |  |  | 0 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| name | varchar | 191 |  √  |  | null |  |
| break | int | 10 |  √  |  | null |  |
| options | json | 1073741824 |  √  |  | null |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| country\_id | Performance | Asc |

## addressvalidation {#addressvalidation}

*This table is used to construct address form (?)*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| addressfield\_id | int | 10 |  |  |  | FK(addressfield) |
| type | varchar | 255 |  |  |  |  |
| value | varchar | 255 |  √  |  | null |  |
| message\_en | varchar | 255 |  |  |  |  |
| message\_ar | varchar | 255 |  |  |  |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
|  |  |  |  |  |  |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| addressfield\_id | Performance | Asc |

## admin {#admin}

*This table stores admin users (including drivers) depending on role*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  |  |
| name | varchar | 255 |  |  |  |  |
| email | varchar | 255 |  |  |  |  |
| password | varchar | 511 |  |  |  |  |
| apple\_id | varchar | 255 |  √  |  | null |  |
| status | bit | 1 |  |  | 1 |  |
| role | int | 10 |  |  | 1 |  |
| target\_id | int | 10 |  √  |  | 0 | ?? |
| is\_deleted | bit | 1 |  |  | 0 |  |
| lastip | varchar | 46 |  √  |  | null |  |
| lastlogin | timestamp | 19 |  √  |  | null |  |
| lastinteract | timestamp | 19 |  √  |  | null |  |
| time | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| phone | varchar | 31 |  |  |  |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| email | Must be unique | Asc |

## admin\_home {#admin_home}

*This table allows admin to preview “home page” without it being available to production/users*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| country\_id | int | 10 |  |  |  | FK(country) |
| home\_id | int | 10 |  √  |  | null | FK(home) |

| Column(s) | Type | Sort |
| :---- | ----- | ----- |
| admin\_id \+ country\_id | Primary key | Asc/Asc |

## admin\_target {#admin_target}

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| target | varchar | 63 |  |  |  | store |
| target\_id | int | 10 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| admin\_id \+ target \+ target\_id | Primary key | Asc/Asc/Asc |

## area {#area}

*This is a lookup table about geographical area of user*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  |  |
| country\_id | int | 10 |  |  |  |  |
| parent\_id | int | 10 |  √  |  | null |  |
| name\_en | varchar | 100 |  √  |  | null |  |
| name\_ar | varchar | 100 |  √  |  | null |  |
| boundary | geometry | 65535 |  √  |  | null |  |
| center | geometry | 65535 |  √  |  | null |  |
| is\_deleted | bit | 1 |  √  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| slug | varchar | 511 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| country\_id \+ is\_deleted \+ parent\_id | Performance | Asc/Asc/Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## asset {#asset}

*This table stores the reference to all documents used in the system e.g. in invoice, etc*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| storage | varchar | 63 |  |  | local |  |
| filename | varchar | 255 |  |  |  |  |
| path | varchar | 255 |  |  |  |  |
| target | varchar | 45 |  √  |  | null |  |
| target\_id | int | 10 |  √  |  | null |  |
| asset\_order | int | 10 |  √  |  | 0 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| target \+ target\_id | Performance | Asc/Asc |
| target \+ target\_id \+ is\_deleted | Performance | Asc/Asc/Asc |

## attribute {#attribute}

*This stores the attribute of products. Right now in the system there are only three attributes: Size, Age, Gender*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| appFilterOp | varchar | 31 |  |  |  |  |
| appFilterItemsOp | varchar | 31 |  |  |  |  |
| secondary\_id | int | 10 |  √  |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| target | varchar | 31 |  |  | product |  |
| slug | varchar | 511 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| is\_deleted | Performance | Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## attributevalue {#attributevalue}

*This table stores the possible values of (product) attribute*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| attribute\_id | int | 10 |  |  |  | FK(attribute) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| color | varchar | 15 |  √  |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| icon | varchar | 255 |  √  |  | null |  |
| slug | varchar | 511 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| attribute\_id \+ is\_deleted | Performance | Asc/Asc |   |
| id \+ attribute\_id | Performance | Asc/Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## badge ☠️ {#badge-☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| color | varchar | 15 |  |  |  |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| country\_id | int | 10 |  |  |  |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## banner {#banner}

*This table stores banner information. Each banner belongs to a slider.* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| slider\_id | int | 10 |  |  |  | FK(slider) |
| name | varchar | 255 |  |  |  |  |
| type | varchar | 50 |  |  |  | category |
| target | json | 1073741824 |  |  |  |  |
| url | varchar | 2047 |  √  |  | null |  |
| status | tinyint | 3 |  |  | 0 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| slug | varchar | 511 |  √  |  | null |  |

| id | Primary key | Asc |   |
| :---- | :---- | :---- | :---- |
| slug | Must be unique | Asc | This unique column is also nullable |

## brand {#brand}

*This table stores brand information **globally** in the system. It can be disabled per country basis via “disabled” table.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| information\_en | varchar | 2047 |  √  |  | null |  |
| information\_ar | varchar | 2047 |  √  |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| displayorder | int | 10 |  |  | 999 |  |
| slug | varchar | 511 |  √  |  | null |  |
| origincountry | varchar | 3 |  √  |  | null |  |
| title\_en | varchar | 255 | √  |  |  |  |
| title\_ar | varchar | 255 | √  |  |  |  |
| description\_en | varchar | 2047 | √  |  |  |  |
| description\_ar | varchar | 2047 | √  |  |  |  |
| notes\_en | varchar | 2047 | √  |  |  |  |
| notes\_ar | varchar | 2047 | √  |  |  |  |
| brand\_type\_id | int | 10 |  |  |  | 0 default, 1 OneCard |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## buyxgety ☠️  {#buyxgety-☠️}

*Unfinished. Unused.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| title | varchar | 255 |  |  |  |  |
| buyx | int | 10 |  |  |  |  |
| gety | int | 10 |  |  |  |  |
| country\_id | int | 10 |  |  |  | FK(country) |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| is\_deleted | bit | 1 |  |  | 0 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## buyxgety\_item ☠️ {#buyxgety_item-☠️}

*Unfinished. Unused.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| buyxgety\_id | int | 10 |  |  |  | FK(buyxgety) |
| item | varchar | 191 |  |  |  |  |
| item\_id | int | 10 |  |  |  |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| buyxgety\_id \+ item \+ item\_id | Must be unique | Asc/Asc/Asc |

## cashflow {#cashflow}

*This table stores money collected from drivers.*

| Name | Comment | Type | Size | Null? | Auto | Default |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | PK | int | 10 |  |  √  |  |
| country\_id | FK(country) | int | 10 |  |  |  |
| admin\_id | FK(admin) | int | 10 |  |  |  |
| giver\_id |  | int | 10 |  √  |  | null |
| type |  | tinyint | 3 |  |  | 1 |
| amount |  | decimal | 10,3 |  |  |  |
| status |  | tinyint | 3 |  |  | 2 |
| options |  | json | 1073741824 |  √  |  | null |
| comment |  | varchar | 255 |  √  |  | null |
| CDate |  | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |
| UDate |  | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## cashflow\_item {#cashflow_item}

*Right now cashflow is only used for delivery/driver. So in this case target is “parcel” which is a unit of processed/delivered order.* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| cashflow\_id | int | 10 |  |  |  | FK(cashflow) |
| target | varchar | 191 |  |  |  | parcel |
| target\_id | int | 10 |  |  |  |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| target \+ target\_id | Must be unique | Asc/Asc |

## category {#category}

*This table stores **global** product category definition for the system. It can be disabled per country basis via “disabled” table.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| color | varchar | 15 |  √  |  | null |  |
| displayorder | int | 10 |  |  | 999 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| text\_color | varchar | 15 |  √  |  | null |  |
| slug | varchar | 511 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## collection {#collection}

*This table stores produce collection information **per country**. A product collection can be **static** or based on dynamic query filter (**smart**)*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| type | bit | 1 |  |  |  | 1 \= static, 2 \= smart |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| is\_disabled | bit | 1 |  |  | 0 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| slug | varchar | 511 |  √  |  | null |  |
| secondaryfilter | varchar | 64 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| id \+ country\_id \+ is\_deleted | Performance | Asc/Asc/Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## collection\_filter {#collection_filter}

*This table stores dynamic filter query information for product collection (collection table) when the collection type is “smart”.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| collection\_id | int | 10 |  |  |  | FK(collection) |
| type | varchar | 31 |  |  |  |  |
| target | varchar | 31 |  |  |  | attribute brand is\_sale tag |
| target\_id | int | 10 |  √  |  | null |  |
| target\_value | varchar | 255 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## collection\_product {#collection_product}

*This table stores information about a product in a collection when the collection type is “static”.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| collection\_id | int | 10 |  |  |  | FK(collection) |
| product\_id | int | 10 |  |  |  | FK(product) |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| collection\_id \+ product\_id | Primary key | Asc/Asc |
| collection\_id | Performance | Asc |

## columnconfig {#columnconfig}

*This table stores column visibility per admin in the management panel.* 

*![][image2]*

*![][image3]*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| page | varchar | 255 |  |  |  |  |
| target | varchar | 255 |  |  |  | action address\_phone admin\_name brand\_name\_en category\_name\_en CDate code color coupon delivery delivery\_date discount download file id image inventory invoice\_id is\_disabled item\_count name\_ar name\_en parcels pay paymentmethod print product\_name\_en range reserved score sku\_count skucount status store stores subcategory\_name\_en subtotal supplier\_name undefined upc user\_name user\_phone wallet |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| is\_visible | bit | 1 |  |  | 1 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| admin\_id \+ page \+ target | Must be unique | Asc/Asc/Asc |

## country {#country}

*This table stores country information in the system. There is no editor for this table. If there is a new country to be added in dabdoob, they need to be added manually.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| dialcode | varchar | 7 |  |  |  |  |
| code2 | char | 2 |  |  |  |  |
| code3 | char | 3 |  |  |  |  |
| flag | char | 2 |  |  |  |  |
| timezone | varchar | 63 |  |  |  |  |
| currencyIso | varchar | 7 |  |  |  |  |
| currency\_en | varchar | 15 |  |  |  |  |
| currency\_ar | varchar | 15 |  |  |  |  |
| decimals | tinyint | 3 |  |  | 3 |  |
| center | geometry | 65535 |  √  |  | null |  |
| tax | decimal | 10,3 |  |  | 0.000 |  |
| contact | varchar | 15 |  |  |  |  |
| address\_en | varchar | 255 |  |  |  |  |
| address\_ar | varchar | 255 |  |  |  |  |
| email | varchar | 127 |  |  |  |  |
| onlyinstock | bit | 1 |  |  | 1 |  |
| showsku | bit | 1 |  |  | 0 |  |
| overrideshipping | bit | 1 |  |  | 0 |  |
| delivery\_days | int | 10 |  |  | 1 |  |
| delivery\_time | time | 8 |  |  | 12:00:00 |  |
| free\_shipping | decimal | 10,3 |  |  | 100.000 |  |
| is\_disabled | bit | 1 |  |  | 1 | If disabled, not visible to to customers |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| taxmode | tinyint | 3 |  |  | 1 |  |
| trn | varchar | 127 |  √  |  | null |  |
| sortinstockfirst | bit | 1 |  |  | 0 |  |
| slug | varchar | 511 |  √  |  | null |  |
| exchange | decimal | 10,6 |  |  | 1.000000 |  |
| area\_type | int | 10 |  |  | 2 |  |
| is\_international | bit | 1 |  |  | 0 |  |
| override\_area\_cost | bit | 1 |  |  | 0 |  |
| inventory\_country | int | 10 |  √  |  | null |  |
| price\_country | int | 10 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| code2 | Must be unique | Asc |   |
| code3 | Must be unique | Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## coupon {#coupon}

*This table stores coupon information **per country**. Todo: figure out how coupon works*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| code | varchar | 63 |  |  |  |  |
| type | varchar | 7 |  |  |  |  |
| amount | decimal | 10,3 |  |  |  |  |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| use\_count | int | 10 |  |  | 1 |  |
| user\_use\_count | int | 10 |  |  | 0 |  |
| firstorder | bit | 1 |  |  | 0 |  |
| fromDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| toDate | timestamp | 19 |  √  |  | null |  |
| description | varchar | 255 |  √  |  | null |  |
| status | bit | 1 |  |  | 1 |  |
| revoke\_reason | varchar | 255 |  √  |  | null |  |
| revoke\_time | timestamp | 19 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| coupongroup\_id | int | 10 |  |  | 0 | FK(Self reference) |
| maximumamount | decimal | 10,3 |  |  | 0.000 |  |
| minimumorder | decimal | 10,3 |  |  | 0.000 |  |
| platforms | json | 1073741824 |  √  |  | null | Array json |
| affiliate | varchar | 255 |  √  |  | null |  |
| freeshipping | bit | 1 |  |  | 0 |  |
| targets | json | 1073741824 |  √  |  | null |  |
| user\_id | int | 10 |  √  |  | null | FK(user) |
| apply\_over\_discount | bit | 1 |  |  | 1 |  |
| is\_sku\_specific  | bit | 1 |  |  | 0 |  |
| is\_user\_specific | bit | 1 |  |  | 0 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| country\_id \+ code | Must be unique | Asc/Asc |
| country\_id \+ coupongroup\_id \+ id | Performance | Asc/Asc/Asc |
| coupongroup\_id \+ id | Performance | Asc/Asc |
| coupongroup\_id | Performance | Asc |
| country\_id \+ code \+ status | Performance | Asc/Asc/Asc |
| status | Performance | Asc |

## coupon\_user {#coupon_user}

This table will store the many to many relation between the coupon and user (for referral reward).

| Name | Type | Size | Null?\! | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| coupon\_id | Int | 10 |  |  |  | FK (coupon) |
| user\_id | Int | 10 |  |  |  | FK (user) |
| CDATE | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s)  | Type | Sort |
| :---- | :---- | :---- |
| coupon\_id \+ sku\_id | Primary key | Asc/Asc |
| coupon\_id  | Performance | Asc |
| user\_id | Performance  | Asc |

## couponsku {#couponsku}

This table will store the many to many relation between the coupon and sku.

| Name | Type | Size | Null?\! | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | Int | 10 |  | √ |  | PK |
| coupon\_id | Int | 10 |  |  |  | FK (coupon) |
| sku\_id | Int | 10 |  |  |  | FK (sku) |
| CDATE | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s)  | Type | Sort |
| :---- | :---- | :---- |
| id | Primary key | Asc |
| coupon\_id \+ sku\_id | Must be unique | Asc/Asc |
| coupon\_id  | Performance | Asc |
| sku\_id  | Performance  | Asc |

## credentials {#credentials}

*For pass keys \- not use for production*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| user\_id | int | 10 |  |  |  | FK(user) |
| name | varchar | 255 |  |  |  |  |
| credential\_id | varchar | 255 |  |  |  |  |
| public\_key | text | 65535 |  |  |  |  |
| counter | int | 10 |  |  | 0 |  |
| transports | json | 1073741824 |  √  |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## creditnote {#creditnote}

*This is related to Wallet.* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| user\_id | int | 10 |  |  |  | FK(user) |
| amount | decimal | 10,3 |  |  | 0.000 |  |
| target | varchar | 31 |  √  |  | null | Can be to invoice, restore |
| target\_id | int | 10 |  √  |  | null |  |
| comment | varchar | 127 |  √  |  | null |  |
| type | tinyint | 3 |  |  | 1 | Possible values are 1 and 2 |
| status | tinyint | 3 |  |  | 2 | Possible values are 0, 1, 2 |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| country\_id | Performance | Asc |

## deliverymethod ☠️ {#deliverymethod-☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| store\_id | int | 10 |  √  |  | null | FK(store) |
| method | varchar | 191 |  |  |  |  |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| subtitle\_en | varchar | 255 |  √  |  | null |  |
| subtitle\_ar | varchar | 255 |  √  |  | null |  |
| options | json | 1073741824 |  √  |  | null |  |
| display\_order | int | 10 |  |  | 99 |  |
| is\_default | bit | 1 |  |  | 0 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| slug | varchar | 511 |  √  |  | null |  |
| secrets | json | 1073741824 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## deliverymethod\_area ☠️ {#deliverymethod_area-☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| deliverymethod\_id | int | 10 |  |  |  | FK(deliverymethod) |
| area\_id | int | 10 |  |  |  | FK(area) |
| cost | decimal | 10,3 |  |  | 0.000 |  |
| is\_shortdistance | bit | 1 |  |  | 0 |  |
| is\_disabled | bit | 1 |  |  | 1 |  |
| options | json | 1073741824 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
|  |  |  |  |  |  |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| deliverymethod\_id \+ area\_id | Must be unique | Asc/Asc |

## deposit {#deposit}

Cash deposit. To do: clarify

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| type | tinyint | 3 |  |  | 1 |  |
| amount | decimal | 10,3 |  |  |  |  |
| status | tinyint | 3 |  |  | 2 | 0 \= deleted, 1 \= done , 2 \= draft |
| reason | varchar | 31 |  √  |  | null |  |
| reason\_id | int | 10 |  √  |  | null |  |
| actor | varchar | 31 |  √  |  | null | admin, supplier |
| actor\_id | int | 10 |  √  |  | null |  |
| method | varchar | 255 |  |  |  | Cash, wire, check (*check dropdown)* |
| description | varchar | 255 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| country\_id | int | 10 |  |  |  | FK(country) |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## device {#device}

*Large table. Each user that connects to the system has an entry in this table.* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int unsigned | 10 |  |  √  |  | PK |
| user\_id | int | 10 |  √  |  | null | FK(user) |
| admin\_id | int | 10 |  √  |  | null | FK(admin) |
| debug | bit | 1 |  |  | 0 |  |
| identifier | varchar | 40 |  |  |  |  |
| bundle | varchar | 255 |  √  |  | null |  |
| token | varchar | 128 |  √  |  | null |  |
| mixpanel\_id | varchar | 255 |  √  |  | null |  |
| status | bit | 1 |  |  | 1 |  |
| notificationToken | varchar | 255 |  √  |  | null |  |
| notificationTokenDev | varchar | 255 |  √  |  | null |  |
| osType | varchar | 20 |  √  |  | null |  |
| osVersion | varchar | 10 |  √  |  | null |  |
| deviceTitle | varchar | 255 |  √  |  | null |  |
| deviceName | varchar | 255 |  √  |  | null |  |
| deviceCapacity | varchar | 63 |  √  |  | null |  |
| version | varchar | 31 |  √  |  | null |  |
| build | int | 10 |  √  |  | null |  |
| env | varchar | 31 |  √  |  | null |  |
| next\_order\_id | varchar | 63 |  √  |  | null |  |
| lastinteract | timestamp | 19 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| language | varchar | 31 |  |  | en |  |
| settings | json | 1073741824 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| user\_id | Performance | Asc |   |
| identifier | Must be unique | Asc |   |
| notificationToken | Performance | Asc |   |
| notificationTokenDev | Performance | Asc |   |
| token | Must be unique | Asc | This unique column is also nullable |

## digital\_gift {#digital_gift}

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| sku\_id | int | 10 |  |  |  | FK (sku) |
| sender\_id | int | 10 |    |  |  | FK(user) |
| receiver\_id | int | 10 | √  |  |  | FK(user) |
| receiver\_name | varchar | 300 | √  |  |  |  |
| receiver\_email | varchar | 300 | √  |  |  |  |
| receiver\_phone\_number | varchar | 63 | √  |  |  |  |
| message | varchar | 255 | √  |  |  |  |
| notification\_method\_id | int | 10 |  |  |  |  |
| status | tinyint | 3 |  |  | 0 | 0: Added to cart 1: Sent 2: Received |
| invoice\_id | int | 10 | √  |  |  | FK(invoice) |
| invoiceItem\_id | int | 10 | √  |  |  | FK(invoiceitem) |
| type | varchar | 63 |  |  |  |  |
| added\_to\_wallet\_date | datetime | 23 | √  |  |  |  |
| sent\_date | timestamp | 19 | √  |  |  |  |
| giftcard\_id | int | 10 | √  |  |  | FK(giftcard) |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## disabled {#disabled}

*This is a rather peculiar table. It is used to mark central entities as disabled for each particular country.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| target | varchar | 45 |  |  |  | brand category justintimeAgreement paymentmethod product subcategory |
| target\_id | int | 10 |  |  |  |  |
| country\_id | int | 10 |  |  |  |  |
| is\_disabled | bit | 1 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| target \+ target\_id \+ country\_id | Primary key | Asc/Asc/Asc |

## donations {#donations}

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| donations\_count | int | 10 |  |  |  |  |
| year | String | 191 |    |  |  |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## dynamicaddress {#dynamicaddress}

*This table holds customer’s address. It is called dynamic because the input for address per country is truly dynamic.* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  |  |
| addresstype\_id | int | 10 |  |  |  |  |
| user\_id | int | 10 |  |  |  |  |
| area\_id | int | 10 |  √  |  | null |  |
| name | varchar | 255 |  |  |  |  |
| text\_en | varchar | 511 |  |  |  |  |
| text\_ar | varchar | 511 |  |  |  |  |
| phone | varchar | 255 |  √  |  | null |  |
| coordinates | varchar | 255 |  √  |  | null |  |
| fields | json | 1073741824 |  |  |  |  |
| address\_id | int | 10 |  √  |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| country\_id | int | 10 |  |  |  |  |
| status\_by\_phone | int | 10 |  |  | 0 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| user\_id \+ country\_id \+ is\_deleted | Performance | Asc/Asc/Asc |
| user\_id \+ is\_deleted | Performance | Asc/Asc |

## entity\_icon ☠️ {#entity_icon-☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  |  |
| target | varchar | 31 |  |  | product |  |
| target\_id | int | 10 |  |  |  |  |
| icon\_id | int | 10 |  |  |  |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| target \+ target\_id \+ icon\_id | Must be unique | Asc/Asc/Asc |

## entitystatus ☠️ {#entitystatus-☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  |  |
| entity | varchar | 31 |  |  |  |  |
| entity\_id | int | 10 |  |  |  |  |
| status | int | 10 |  |  |  |  |
| kind | varchar | 31 |  |  |  |  |
| user\_id | int | 10 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## exchange ☠️ {#exchange-☠️}

*Unused. The idea was to handle foreign currency conversion on price.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  |  |
| country\_id | int | 10 |  |  |  |  |
| exchange | decimal | 10,6 |  |  | 1.000000 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## faq ☠️ {#faq-☠️}

*Unused. FAQs are static now.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  |  |
| question\_en | varchar | 1023 |  |  |  |  |
| question\_ar | varchar | 1023 |  |  |  |  |
| answer\_en | longtext | 2147483647 |  |  |  |  |
| answer\_ar | longtext | 2147483647 |  |  |  |  |
| order | int | 10 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| is\_deleted | bit | 1 |  |  | 0 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## featureannouncement {#featureannouncement}

*This is used to announce new features in the management panel*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| name | varchar | 100 |  √  |  | null |  |
| message | varchar | 255 |  √  |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| permitions | varchar | 100 |  √  |  | null |  |
| link | varchar | 100 |  √  |  | null |  |
| comment | varchar | 255 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## featureannouncement\_admin {#featureannouncement_admin}

*Each receiving admin of a feature announcement will have an entry here*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| announcement\_id | int | 10 |  |  |  | FK(featureannouncement) |
| seen | tinyint | 3 |  |  | 0 |  |
| status | tinyint | 3 |  |  | 1 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| announcement\_id | Performance | Asc |

## featuredcollection ☠️ {#featuredcollection-☠️}

Unused

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| collection\_id | int | 10 |  |  |  | FK(collection) |
| status | int | 10 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## giftcard {#giftcard}

*This table holds instances of a giftcard. Each row represents one giftcard.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| code | varchar | 63 |  |  |  |  |
| amount | decimal | 10,3 |  |  |  |  |
| admin\_id | int | 10 |  √  |  | null | FK(admin) |
| description | varchar | 255 |  √  |  | null |  |
| status | tinyint | 3 |  |  | 1 | if\_case("status",-1,' Bought By Customer',0,'Used', 1,'Not Used') (From Zoho) |
| revoke\_reason | varchar | 255 |  √  |  | null |  |
| revoke\_time | timestamp | 19 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| giftcardoption\_id | int | 10 |  √  |  | null |  |
| transaction\_id | int | 10 |  √  |  | null |  |
| user\_id | int | 10 |  √  |  | null |  |
| is\_user\_specific | bit | 1 |  |  | 0 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| admin\_id | Performance | Asc |
| country\_id \+ code | Must be unique | Asc/Asc |
| status | Performance | Asc |

## giftcardoption {#giftcardoption}

*This table stores gift card’s amount **per country**.* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| amount | decimal | 10,3 |  |  |  |  |
| displayorder | int | 10 |  |  | 999 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## hit {#hit}

*This is a large table. The data gets flushed on a regular basis.* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| device\_id | int | 10 |  √  |  | null | FK(device) |
| user\_id | int | 10 |  √  |  | null | FK(user) |
| target | varchar | 31 |  |  |  | product |
| target\_id | int | 10 |  |  |  |  |
| time | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| target \+ device\_id \+ time | Performance | Asc/Asc/Desc |
| target \+ user\_id \+ time | Performance | Asc/Asc/Desc |
| time | Performance | Desc |

## 

## 

## 

## 

## 

## 

## 

## home {#home}

*This table stores home page information **per country**.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| is\_active | bit | 1 |  |  | 0 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| slug | varchar | 511 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| is\_active \+ country\_id \+ is\_deleted | Performance | Asc/Asc/Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## homepage {#homepage}

*This table stores widget that appears at the home page. Todo: verify*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| home\_id | int | 10 |  |  |  | FK(home) |
| display\_order | int | 10 |  |  | 0 |  |
| title\_text\_en | varchar | 255 |  √  |  | null |  |
| title\_text\_ar | varchar | 255 |  √  |  | null |  |
| color | varchar | 15 |  √  |  | null |  |
| target | varchar | 255 |  √  |  | null | brand category product product2 slider video\_sku widget |
| target\_list | json | 1073741824 |  √  |  | null |  |
| options | json | 1073741824 |  √  |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| is\_visible | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## icon☠️  {#icon☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| target | varchar | 31 |  |  | product |  |
| color | varchar | 15 |  √  |  | null |  |
| icon | varchar | 255 |  √  |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| id \+ is\_deleted | Performance | Asc/Asc |

## identity☠️ {#identity☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  |  |
| user\_id | int | 10 |  |  |  |  |
| identity | varchar | 63 |  |  |  |  |
| old | varchar | 1023 |  √  |  | null |  |
| value | varchar | 1023 |  |  |  |  |
| status | tinyint | 3 |  |  | 0 |  |
| hash | varchar | 255 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

##  inventory {#inventory}

*This table stores 1 : 1 correlation with actual product items.  So if there are 1000 teddy bears, there will be 1000 entries in this table.* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| cost | decimal | 10,3 |  |  | 0.000 |  |
| document\_id | int | 10 |  |  |  | FK(inventorydocument)f |
| sold | varchar | 15 |  √  |  | null | Invoice, document (if null, product on the shelf) |
| sold\_id | int | 10 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| expiry\_date | datetime | 23 |  √  |  | null |  |
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

## inventorydocument {#inventorydocument}

*This table stores warehouse(Store) inventory related documents (PO, Purchase Return). Todo review.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| store\_id | int | 10 |  |  |  | FK(store) |
| supplier\_id | int | 10 |  |  |  | FK(supplier) |
| po\_id | int | 10 |  √  |  | null | FK(self reference) |
| comment | varchar | 511 |  √  |  | null |  |
| type | tinyint | 3 |  |  | 1 | 1 \= PO, \-1 \= Purchase Return |
| agreement | tinyint | 3 |  |  | 1 | 1 \= Purchase, 2 \= Consignment |
| status | tinyint | 3 |  |  | 2 | 1\. done, published 	 2\. draft 	 3\. sent 	 \-1. supplier rejected 	 0\. deleted draft, 	 4\. supplier or admin accepted 	 5\. delivered 	 6\. partially delivered |
| count | int | 10 |  |  | 0 | The number of SKU created by this PO (10 \= 10 rows in inventory table) |
| cost | decimal | 10,3 |  |  | 0.000 | Total cost of all the items |
| publisher\_id | int | 10 |  √  |  | null | FK(admin) |
| published\_time | timestamp | 19 |  √  |  | null |  |
| helper | json | 1073741824 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| adjustment | tinyint | 3 |  |  | 0 |  |
| referenceno | varchar | 511 |  √  |  | null | If PO, this is required |
| vat | decimal | 10,3 |  |  | 0.000 | Actual amount of VAT  |
| jit\_id | int | 10 |  √  |  | null | FK(justintimeagreement) |
| payment\_due\_date | datetime | 23 |  √  |  | null |  |
| batchno | varchar | 511 |  √  |  | null | *Not used* |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| admin\_id | Performance | Asc |
| id \+ store\_id \+ supplier\_id | Performance | Asc/Asc/Asc |
| status \+ id \+ store\_id | Performance | Asc/Asc/Asc |
| status \+ store\_id | Performance | Asc/Asc |
| store\_id | Performance | Asc |
| store\_id \+ id | Performance | Asc/Asc |
| type \+ store\_id \+ id \+ cost | Performance | Asc/Asc/Asc/Asc |

## inventorydraft {#inventorydraft}

*TBC*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| cost | decimal | 10,3 |  √  |  | null |  |
| document\_id | int | 10 |  |  |  | FK(inventorydocument) |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| expiry\_date | datetime | 23 |  √  |  | null |  |
| vat | decimal | 10,3 |  |  | 0.000 | Actual amount  |
| vatperc | decimal | 10,2 |  |  | 0.00 | VAT Percentage |
| is\_deleted | bit | 1 |  |  | 0 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| document\_id | Performance | Asc |
| document\_id \+ sku\_id | Performance | Asc/Asc |
| sku\_id | Performance | Asc |

## invoice {#invoice}

*This table stores the order that customers made in the front end. The store frontend stores the shopping card separately. When the order is submitted, an invoice is generated.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| device\_id | int | 10 |  |  |  | FK(device) |
| user\_id | int | 10 |  |  |  | FK(user) |
| coupon\_id | int | 10 |  √  |  | null | FK(coupon) |
| address\_id | int | 10 |  |  |  | FK(dynamicaddress) |
| paymentmethod\_id | int | 10 |  |  |  | FK(paymentmethod) |
| subtotal | decimal | 10,3 |  |  |  |  |
| discount | decimal | 10,3 |  |  | 0.000 |  |
| delivery | decimal | 10,3 |  |  | 0.000 |  |
| pay | decimal | 10,3 |  |  |  | The actual amount that the custthat the customer pays |
| tax | decimal | 10,3 |  |  | 0.000 | VAT value |
| profit | decimal | 10,3 |  |  | 0.000 |  |
| payment\_commission | decimal | 10,3 |  |  | 0.000 |  |
| paymentStatus | tinyint | 3 |  |  | 0 | 1 \= Paid, \-1 \= Expired \=0 \= Not Paid |
| deliveryStatus | bit | 1 |  |  | 0 | 0 \=1 \= delivered, 0 \= else |
| status | tinyint | 3 |  |  | 1 |  1  \= default,  \-1  \= cancelled \-2 \= Error When inventoryModel.cancelInvoice(...) is called When inventory.sell(...) fails for any reason When paymentService.createTransaction(...) fails for any reason |
| code | varchar | 63 |  |  |  | Generated from device table |
| parcelJson | json | 1073741824 |  √  |  | null | Heavily used |
| routeJson | json | 1073741824 |  √  |  | null |  |
| paymentInitJson | json | 1073741824 |  √  |  | null | unused |
| paymentResJson | json | 1073741824 |  √  |  | null | unused |
| fatoora\_id | int | 10 |  √  |  | null | unused |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| EDate | timestamp | 19 |  |  |  | Expired date of this invoice |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| wallet | decimal | 10,3 |  |  | 0.000 |  |
| admin\_id | int | 10 |  √  |  | null | FK(admin) \- admin created this invoice |
| adminComment | varchar | 2047 |  √  |  | null |  |
| userComment | varchar | 2047 |  √  |  | null |  |
| cancelStatus | tinyint | 3 |  |  | 0 | 0 \= nothing, 2 partially cancelled , \= 1 \= fully cancelled |
| applytax | decimal | 10,3 |  |  | 0.000 |  |
| cost | decimal | 10,3 |  |  | 0.000 |  |
| source | varchar | 63 |  √  |  | null |  |
| promo\_coupon\_id | varchar | 255 | √  |  | null | Coupon id from promo engine |

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

## invoiceItem {#invoiceitem}

*This table stores the product item that a customer orders*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| invoice\_id | int | 10 |  |  |  | FK(invoice) |
| invoiceParcel\_id | int | 10 |  |  |  | FK(invoiceparcel) |
| inventory\_id | int | 10 |  |  |  | FK(inventory) \- exact row of product sold |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| store\_id | int | 10 |  |  |  | FK(store) |
| price | decimal | 10,3 |  |  |  |  |
| cost | decimal | 10,3 |  |  |  |  |
| sku | json | 1073741824 |  |  |  |  |
| wrapping | json | 1073741824 |  √  |  | null |  |
| wrapping\_id | int | 10 |  √  |  | null | FK(wrapping) |
| wrapping\_price | decimal | 10,3 |  |  | 0.000 |  |
| cardFrom | varchar | 255 |  √  |  | null |  |
| cardTo | varchar | 255 |  √  |  | null |  |
| cardMessage | varchar | 1023 |  √  |  | null |  |
| restore\_id | int | 10 |  √  |  | null | FK(restore) \- wused when performaing order return |
| customtext | text | 65535 |  √  |  | null |  |
| old\_price | decimal | 10,3 |  √  |  | null |  |
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

## invoiceparcel (not used) {#invoiceparcel-(not-used)}

*TBC*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| invoice\_id | int | 10 |  |  |  | FK(invoice) |
| store\_id | int | 10 |  |  |  | FK(store) |
| delivery\_date | date | 10 |  |  |  |  |
| delivery\_cost | decimal | 10,3 |  |  |  | Teh cost of delivery from warehouse |
| subtotal | decimal | 10,3 |  |  | 0.000 |  |
| discount | decimal | 10,3 |  |  | 0.000 |  |
| pay | decimal | 10,3 |  |  | 0.000 |  |
| tax | decimal | 10,3 |  |  | 0.000 |  |
| profit | decimal | 10,3 |  |  | 0.000 |  |
| delivery | decimal | 10,3 |  |  | 0.000 |  |
| status | int | 10 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| wallet | decimal | 10,3 |  |  | 0.000 |  |
| deliveryJson | json | 1073741824 |  √  |  | null |  |
| deliverymethod\_id | int | 10 |  √  |  | null | todo? |
| timeslot\_id | int | 10 |  √  |  | null | FK(timeslot), not used |
| deliveryDate | timestamp | 19 |  √  |  | null |  |
| deliveryEstimate | timestamp | 19 |  √  |  | null |  |
| deliveryEstimateEnd | timestamp | 19 |  √  |  | null |  |
| cost | decimal | 10,3 |  |  | 0.000 |  |
| payment\_commission | decimal | 10,3 |  |  | 0.000 |  |
| adminComment | varchar | 2047 |  √  |  | null |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| id \+ status | Performance | Asc/Asc |
| id \+ store\_id | Performance | Asc/Asc |
| invoice\_id | Performance | Asc |
| invoice\_id \+ id | Performance | Asc/Asc |
| invoice\_id \+ store\_id \+ id | Performance | Asc/Asc/Asc |
| status \+ store\_id \+ id | Performance | Asc/Asc/Asc |

## invoiceparcel\_admin {#invoiceparcel_admin}

*Todo: it might be about the kanban*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| parcel\_id | int | 10 |  |  |  | FK(parcel) |
| parcel\_status | int | 10 |  |  |  |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| is\_deleted \+ admin\_id \+ parcel\_status | Performance | Asc/Asc/Asc |
| parcel\_id \+ parcel\_status \+ is\_deleted \+ id | Performance | Asc/Asc/Asc/Asc |

## itemorder\_country {#itemorder_country}

*This table stores custom sort information per country.*

![][image4]

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| target | varchar | 191 |  |  |  |  |
| target\_id | int | 10 |  |  |  |  |
| displayorder | int | 10 |  |  |  |  |
| country\_id | int | 10 |  |  |  |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| target \+ target\_id \+ country\_id | Must be unique | Asc/Asc/Asc |

## justintimeagreement {#justintimeagreement}

*This table stores information about just in time agreement. This is a form of dropshipping. This allows dabdoob to sell products without having to keep them in inventory. For example, birthday cake. Obviously there is no cake in inventory.* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| supplier\_id | int | 10 |  |  |  | FK(supplier) |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| warehouse\_id | int | 10 |  |  |  |  |
| country\_id | int | 10 |  |  |  | FK(country) |
| comment | varchar | 511 |  √  |  | null |  |
| expiry\_date | datetime | 23 |  |  |  |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| *Column(s)* | *Type* | *Sort* |
| ----- | ----- | ----- |
| *id* | *Primary key* | *Asc* |

## landing☠️ {#landing☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  √  |  | null | FK(country) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| description\_en | varchar | 4095 |  √  |  | null |  |
| description\_ar | varchar | 4095 |  √  |  | null |  |
| type | varchar | 31 |  |  | normal |  |
| target | varchar | 31 |  √  |  | null |  |
| target\_id | int | 10 |  √  |  | null |  |
| action | json | 1073741824 |  √  |  | null |  |
| background | json | 1073741824 |  √  |  | null |  |
| options | json | 1073741824 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| is\_deleted | bit | 1 |  |  | 0 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## legacyusers☠️ {#legacyusers☠️}

*Unused. It used to store login info from the old codebase.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  |  | PK |
| name | varchar | 255 |  |  |  |  |
| mobile | varchar | 255 |  |  |  |  |
| email | varchar | 255 |  |  |  |  |
| password | varchar | 255 |  |  |  |  |
| clearpassword | varchar | 255 |  |  |  |  |
| hashId | varchar | 255 |  |  |  |  |
| status | tinyint | 3 |  √  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## 

## 

## main\_banner {#main_banner}

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| name | varchar | 255 |  |  |  |  |
| type | varchar | 50 |    |  |  |  |
| target |  | 10 |  |  |  |  |
| url | varchar | 2047 | √  |  |  |  |
| status | tinyint |  |  |  | 0 |  |
| is\_deleted | bit |  |  |  | false |  |
| slug | varchar | 511 | √ |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## media {#media}

*This table stores the reference to all images or video used in the system e.g. in products, etc*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| storage | varchar | 63 |  |  | local |  |
| type | varchar | 15 |  |  | image | Or video” |
| path | varchar | 255 |  |  |  |  |
| target | varchar | 45 |  √  |  | null | banner banner\_ar banner\_ar\_gif banner\_en\_gif brand category\_ar category\_en categoryIcon country giftcardoption notifyOffer paymentmethod sku widget\_ar widget\_en wrapping |
| target\_id | int | 10 |  √  |  | null |  |
| image\_order | int | 10 |  √  |  | 0 |  |
| resize | json | 1073741824 |  √  |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| blurhash | varchar | 45 |  √  |  | null |  |
| format | varchar | 15 |  √  |  | null |  |
| height | int | 10 |  √  |  | null |  |
| metadata | json | 1073741824 |  √  |  | null |  |
| size | int | 10 |  √  |  | null |  |
| width | int | 10 |  √  |  | null |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| target \+ target\_id | Performance | Asc/Asc |
| is\_deleted \+ target\_id | Performance | Asc/Asc |
| target \+ target\_id \+ is\_deleted | Performance | Asc/Asc/Asc |

## notify {#notify}

*This table stores customers’ preference to be notified when a product is in stock. This is once off. So if a customer ask to be notified for a product availability and then they were notified, they will no longer be notified the next time around. They will have to ask again to be notified.* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| user\_id | int | 10 |  √  |  | null | FK(user) |
| email | varchar | 255 |  √  |  | null |  |
| status | bit | 1 |  |  | 1 | 1 \= to benotified, \-1 \= dp, 0 \= was notified |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| area\_id | int | 10 |  √  |  | null | FK(area) |
| country\_id | int | 10 |  √  |  | null | FK(country) |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| sku\_id \+ user\_id \+ area\_id \+ status | Performance | Asc/Asc/Asc/Asc |

## notify\_offers {#notify_offers}

*This table is used to push notification for offers for apps*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| name | varchar | 100 |  √  |  | null |  |
| message | json | 1073741824 |  √  |  | null |  |
| status | tinyint | 3 |  |  | 1 |  |
| coupon\_id | int | 10 |  |  |  | FK(coupon) |
| segment | json | 1073741824 |  √  |  | null |  |
| message\_sent\_date | timestamp | 19 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## nubox ☠️ {#nubox-☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| count | int | 10 |  |  |  |  |
| discount | decimal | 10,2 |  |  |  |  |
| height | decimal | 10,2 |  √  |  | null |  |
| length | decimal | 10,2 |  √  |  | null |  |
| weight | decimal | 10,2 |  √  |  | null |  |
| width | decimal | 10,2 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| is\_deleted | bit | 1 |  |  | 0 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| sku\_id | Performance | Asc |

## outlet ☠️ {#outlet-☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| address | varchar | 511 |  |  |  |  |
| lat | double | 22 |  |  |  |  |
| lng | double | 22 |  |  |  |  |
| phone | varchar | 31 |  √  |  | null |  |
| country\_id | int | 10 |  |  |  | FK(country) |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| is\_deleted | bit | 1 |  |  | 0 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## paymentmethod {#paymentmethod}

*TBC*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| disabledtext\_en | varchar | 255 |  |  |  |  |
| disabledtext\_ar | varchar | 255 |  |  |  |  |
| endpoint | varchar | 255 |  √  |  | null |  |
| secret1 | text | 65535 |  √  |  | null |  |
| secret2 | text | 65535 |  √  |  | null |  |
| secret3 | text | 65535 |  √  |  | null |  |
| commission | float | 12 |  |  | 0 |  |
| display\_order | int | 10 |  |  | 99 |  |
| is\_default | bit | 1 |  |  | 0 |  |
| is\_hidden | bit | 1 |  |  | 0 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| method | varchar | 63 |  |  |  |  |
| slug | varchar | 511 |  √  |  | null |  |
| options | json | 1073741824 |  √  |  | null |  |
| identifier | varchar | 255 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## permission {#permission}

*This table stores management panel permission information per role and **per country**.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| role\_id | int | 10 |  |  |  | FK(role) |
| country\_id | int | 10 |  |  |  | FK(country) |
| permission | varchar | 63 |  |  |  |  |
| target | varchar | 63 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| role\_id \+ country\_id \+ permission \+ target | Must be unique | Asc/Asc/Asc/Asc |

## pricecampaign ☠️ {#pricecampaign-☠️}

*Unused. Incomplete.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| collection\_id | int | 10 |  √  |  | null | FK(collection) |
| fixedPerc | decimal | 10,2 |  √  |  | null |  |
| startDate | timestamp | 19 |  |  |  |  |
| endDate | timestamp | 19 |  √  |  | null |  |
| comment | varchar | 511 |  √  |  | null |  |
| status | tinyint | 3 |  |  | 2 |  |
| is\_disabled | bit | 1 |  |  | 1 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## pricecampaign\_sku ☠️ {#pricecampaign_sku-☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| priceCampaign\_id | int | 10 |  |  |  | FK(pricecampaign) |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| price | decimal | 10,3 |  |  |  |  |
| old\_price | decimal | 10,3 |  √  |  | null |  |
| perc | decimal | 10,2 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| priceCampaign\_id \+ sku\_id | Primary key | Asc/Asc |

## pricehistory {#pricehistory}

*This table keeps track of price history changes*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| price | decimal | 10,3 |  |  |  |  |
| old\_price | decimal | 10,3 |  √  |  | null |  |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## pricing ☠️ {#pricing-☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| quantity | int | 10 |  |  |  |  |
| discount | decimal | 10,2 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| is\_deleted | bit | 1 |  |  | 0 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## product {#product}

*This table store **global** information about product in the system*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| sku\_id | int | 10 |  √  |  | null | FK(sku) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| description\_en | varchar | 4095 |  |  |  |  |
| description\_ar | varchar | 4095 |  |  |  |  |
| nutrition\_en | varchar | 2047 |  √  |  | null |  |
| nutrition\_ar | varchar | 2047 |  √  |  | null |  |
| subcategory\_id | int | 10 |  |  |  | FK(subcategory) |
| brand\_id | int | 10 |  |  |  | FK(brand) |
| is\_wrappable | bit | 1 |  |  | 1 | 1 \= wrapable, 0 \= not |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| upc | varchar | 31 |  √  |  | null |  |
| skucount | int | 10 |  |  | 0 |  |
| origincountry | varchar | 3 |  √  |  | null | unused |
| allergicnote\_ar | text | 65535 |  √  |  | null | unused |
| allergicnote\_en | text | 65535 |  √  |  | null | unused |
| is\_shortdistance | bit | 1 |  |  | 0 | unused |
| is\_customizable | bit | 1 |  |  | 0 |  |
| slug | varchar | 511 |  √  |  | null |  |
| howtouse\_ar | text | 65535 |  √  |  | null | unused |
| howtouse\_en | text | 65535 |  √  |  | null | unused |
| is\_international | bit | 1 |  |  | 0 | unused |
| is\_digital | bit | 1 |  |  | false |  |
| disable\_cash | bit | 1 |  |  | false |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| brand\_id \+ is\_deleted | Performance | Asc/Asc |   |
| is\_deleted \+ id | Performance | Asc/Asc |   |
| subcategory\_id | Performance | Asc |   |
| subcategory\_id \+ brand\_id | Performance | Asc/Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |
| upc | Must be unique | Asc | This unique column is also nullable |
| is\_digital | Performance |  |  |

## product\_attributevalue {#product_attributevalue}

*This table stores product  attribute values. Currently there are three attributes (Size, Gender, Age).* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| product\_id | int | 10 |  |  |  |  |
| attributevalue\_id | int | 10 |  |  |  |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| product\_id \+ attributevalue\_id | Primary key | Asc/Asc |

## product\_badge {#product_badge}

*Unused.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| product\_id | int | 10 |  |  |  | FK(product) |
| badge\_id | int | 10 |  |  |  | FK(badge) |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| product\_id | Performance | Asc |
| badge\_id | Performance | Asc |
| product\_id \+ badge\_id | Must be unique | Asc/Asc |

## productfavorite {#productfavorite}

*Unused. This table stores customers’ favorited product information. API is ready but not implemented in client.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| product\_id | int | 10 |  |  |  | FK(product) |
| user\_id | int | 10 |  |  |  | FK(user) |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| product\_id \+ user\_id | Must be unique | Asc/Asc |

## relatedproduct ☠️ {#relatedproduct-☠️}

*Unused. This table stores global related product information.* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| product\_id | int | 10 |  |  |  | FK(product) |
| related\_product\_id | int | 10 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| product\_id \+ related\_product\_id | Must be unique | Asc/Asc |

## relatedtableconfig {#relatedtableconfig}

*This table stores admin’s related table showing preference in the management panel.*

*![][image5]*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| page | varchar | 255 |  |  |  |  |
| table | varchar | 255 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| is\_visible | bit | 1 |  |  | 1 |  |
| displayorder | int | 10 |  |  | 0 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| admin\_id \+ page \+ table | Must be unique | Asc/Asc/Asc |

## resetHash {#resethash}

*This table is used in change password (random string) process.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| target | varchar | 31 |  |  | user | admin user |
| target\_id | int | 10 |  |  |  |  |
| hash | varchar | 255 |  |  |  |  |
| status | bit | 1 |  |  | 1 |  |
| expire | timestamp | 19 |  √  |  | null |  |
| time | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## restore {#restore}

*This has something to do with inventory. Order Return in the panel.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| invoice\_id | int | 10 |  |  |  | FK(invoice) |
| po\_id | int | 10 |  √  |  | null | *unused* |
| comment | varchar | 2047 |  √  |  | null |  |
| status | tinyint | 3 |  |  | 2 | 0 → Deleted 1 → Published 2 → Draft 3 → Sent 4 → Accepted \-1 → Rejected |
| count | int | 10 |  |  | 0 |  |
| cost | decimal | 10,3 |  |  | 0.000 |  |
| helper | json | 1073741824 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| admin\_id | Performance | Asc |
| country\_id | Performance | Asc |
| status | Performance | Asc |

## restoreitem {#restoreitem}

*This table keeps track of Order Return Item.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| invoiceItem\_id | int | 10 |  |  |  | FK(invoiceitem) |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| store\_id | int | 10 |  |  |  | FK(store) |
| restore\_id | int | 10 |  |  |  | FK(restore) |
| cost | decimal | 10,3 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| type | tinyint | 3 |  |  | 1 | 0 \= defected,  2 \= return to supplier,  1 \= return to warehouse |

## role {#role}

*This table stores role information in the system.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| name | varchar | 255 |  |  |  |  |
| type | varchar | 31 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## search ☠️ {#search-☠️}

*Unused. Has data but not used/turned off. It has been replaced by ElasticSearch.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| device\_id | int | 10 |  |  |  | FK(device) |
| user\_id | int | 10 |  √  |  | null | FK(user) |
| term | varchar | 2023 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| country\_id | int | 10 |  √  |  | null | FK(country) |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| country\_id \+ device\_id \+ term \+ CDate | Performance | Asc/Asc/Asc/Asc |
| country\_id \+ term | Performance | Asc/Asc |
| country\_id \+ term \+ CDate | Performance | Asc/Asc/Asc |
| country\_id \+ user\_id \+ term \+ CDate | Performance | Asc/Asc/Asc/Asc |

## setting {#setting}

*This table is used to store setting information.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| entity | varchar | 191 |  |  |  |  |
| entity\_id | int | 10 |  |  |  |  |
| item | varchar | 191 |  |  |  |  |
| value | varchar | 191 |  |  |  |  |
| casting\_type | varchar | 191 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| item \+ entity \+ entity\_id | Primary key | Asc/Asc/Asc |

## short\_deep\_url {#short_deep_url}

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| long\_url | String | 1000 |  |  |  | FK(country) |
| short\_url | String | 200 |  |  |  | Unique |
| expired\_at | timestamp | 10 |   √  |  |  |  |
| expired\_at\_timezone | String | 80 | √ |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| short\_url | Unique | None |

## shortcut ☠️ {#shortcut-☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| parent | varchar | 63 |  |  | default |  |
| country\_id | int | 10 |  |  |  | FK(country) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| type | varchar | 63 |  |  |  |  |
| target | json | 1073741824 |  √  |  | null |  |
| url | varchar | 1023 |  √  |  | null |  |
| displayorder | int | 10 |  |  | 999 |  |
| is\_disabled | bit | 1 |  |  | 0 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| slug | varchar | 511 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## sku {#sku}

*This table stores the information about SKU (stock keeping unit)*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| product\_id | int | 10 |  |  |  | FK(product) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| code | varchar | 127 |  √  |  | null | Not used anymore |
| color | varchar | 15 |  √  |  | \#000000 |  |
| limit | int | 10 |  |  | 999 | Buy limit for a customer in ordorder |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| item\_number | varchar | 127 |  √  |  | null | Internal Dabdoob code |
| upc | varchar | 31 |  √  |  | null |  |
| height | decimal | 10,2 |  √  |  | null | Not used |
| length | decimal | 10,2 |  √  |  | null | Not used |
| weight | decimal | 10,2 |  √  |  | null | Not used |
| width | decimal | 10,2 |  √  |  | null | Not used |
| box\_count | int | 10 |  |  | 1 | Not used |
| box\_name\_en | varchar | 127 |  √  |  | null | Not used |
| box\_name\_ar | varchar | 127 |  √  |  | null | Not used |
| ref\_sku\_id | int | 10 |  √  |  | null | Not used |
| allergicnote\_ar | text | 65535 |  √  |  | null | Not used |
| allergicnote\_en | text | 65535 |  √  |  | null | Not used |
| ingredient\_ar | varchar | 2047 |  √  |  | null | Not used |
| ingredient\_en | varchar | 2047 |  √  |  | null | Not used |
| slug | varchar | 511 |  √  |  | null | Used |
| minorder | int | 10 |  |  | 1 |  |
| unit | varchar | 63 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| code | Must be unique | Asc | This unique column is also nullable |
| is\_deleted \+ id \+ product\_id | Performance | Asc/Asc/Asc |   |
| is\_deleted \+ id \+ ref\_sku\_id | Performance | Asc/Asc/Asc |   |
| product\_id \+ id | Performance | Asc/Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |
| upc | Must be unique | Asc | This unique column is also nullable |

## sku\_attributevalue ☠️  {#sku_attributevalue-☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| attributevalue\_id | int | 10 |  |  |  | FK(attributevalue) |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| sku\_id \+ attributevalue\_id | Primary key | Asc/Asc |

## sku\_country {#sku_country}

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| country\_id | int | 10 |  |  |  | FK(country) |
| price | decimal | 10,3 |  |  |  |  |
| old\_price | decimal | 10,3 |  √  |  | null |  |
| is\_disabled | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| score | int | 10 |  |  | 100 | Custom sorting |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| country\_id \+ is\_disabled | Performance | Asc/Asc |
| sku\_id \+ country\_id | Must be unique | Asc/Asc |

## sku\_suggestiongroup {#sku_suggestiongroup}

*TBD*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| suggestionGroup\_id | int | 10 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| suggestionGroup\_id \+ sku\_id | Performance | Asc/Asc |

## slider {#slider}

*This table contains slider definitions. Each slider can contain multiple banners.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| is\_disabled | bit | 1 |  |  | 1 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| slug | varchar | 511 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## smsprovider {#smsprovider}

*This table stores information about SMS providers used in the system. Currently Dabodoob uses 3 providers (FCC, Kuwait SMS, Infobit)*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| dialcodes | json | 1073741824 |  |  |  |  |
| title | varchar | 255 |  |  |  |  |
| endpoint | varchar | 1023 |  √  |  | null |  |
| secrets | json | 1073741824 |  √  |  | null |  |
| options | json | 1073741824 |  √  |  | null |  |
| priority | int | 10 |  |  | 99 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| method | varchar | 63 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| is\_disabled | bit | 1 |  |  | 0 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## smsprovider\_log {#smsprovider_log}

*This table stores every sms sent* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| smsprovider\_id | int | 10 |  |  |  | FK(smsprovider) |
| url | varchar | 2047 |  |  |  |  |
| bodyJson | json | 1073741824 |  √  |  | null |  |
| responseJson | json | 1073741824 |  √  |  | null |  |
| updateJson | json | 1073741824 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## snapshot\_inventory  {#snapshot_inventory}

*Refreshed every 5 minutes (for management panel). For actual sales, use inventory table*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| pk | int | 10 |  |  √  |  | PK |
| id | int | 10 |  |  |  |  |
| product\_id | int | 10 |  |  |  | FK(product) |
| name\_en | varchar | 255 |  |  |  |  |
| code | varchar | 127 |  √  |  | null |  |
| limit | int | 10 |  |  | 999 |  |
| item\_number | varchar | 127 |  √  |  | null |  |
| upc | varchar | 31 |  √  |  | null |  |
| slug | varchar | 511 |  √  |  | null |  |
| unit | varchar | 63 |  √  |  | null |  |
| expiry\_date | datetime | 23 |  √  |  | null |  |
| product\_name\_en | varchar | 255 |  |  |  |  |
| product\_upc | varchar | 31 |  √  |  | null |  |
| store\_available | int | 10 |  |  |  |  |
| doc\_in | int | 10 |  |  |  |  |
| doc\_out | int | 10 |  |  |  |  |
| store\_reserve | int | 10 |  |  |  |  |
| store\_value | decimal | 10,3 |  |  |  |  |
| store\_sold | int | 10 |  |  |  |  |
| store\_defect | int | 10 |  |  |  |  |
| store\_return | int | 10 |  |  |  |  |
| store\_id | int | 10 |  |  |  | FK(store) |
| supplier\_id | int | 10 |  |  |  | FK(supplier) |
| doc\_out\_value | decimal | 10,3 |  |  |  |  |
| expiry\_date\_helper | int unsigned | 10 |  √  |  | null |  |
| store\_hold | int | 10 |  |  | 0 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| pk | Primary key | Asc |
| store\_id \+ id \+ product\_id \+ name\_en \+ code \+ limit | Performance | Asc/Asc/Asc/Asc/Asc/Asc |
| id \+ expiry\_date\_helper \+ store\_id \+ supplier\_id | Must be unique | Asc/Asc/Asc/Asc |

## staticpage {#staticpage}

*This page is used to store HTML definition of static pages such as About us, privacy, etc*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| alias | varchar | 255 |  |  |  |  |
| title\_en | varchar | 255 |  |  |  |  |
| title\_ar | varchar | 255 |  |  |  |  |
| html\_en | text | 65535 |  |  |  |  |
| html\_ar | text | 65535 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| country\_id | int | 10 |  |  | 0 | FK(country) |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## statushistory {#statushistory}

*This table stores status history for Parcel. In theory it can store status of other entities but practically it only stores parcel.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| target | varchar | 31 |  |  |  | Always “parcel” |
| target\_id | int | 10 |  |  |  |  |
| status | int | 10 |  |  |  |  |
| admin\_id | int | 10 |  |  |  | FK(admin) |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| duration | int | 10 |  √  |  | null |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| CDate | Performance | Desc |
| target \+ target\_id \+ status \+ CDate | Performance | Asc/Asc/Asc/Desc |

## store {#store}

*This table stores warehouse information. There could be multiple warehouses per country.* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| phone | varchar | 31 |  √  |  | null |  |
| address | varchar | 255 |  √  |  | null |  |
| lat | double | 22 |  |  |  |  |
| lng | double | 22 |  |  |  |  |
| delivery\_days | int | 10 |  |  | 1 |  |
| delivery\_time | time | 8 |  |  | 12:00:00 |  |
| free\_shipping | decimal | 10,3 |  |  | 100.000 | Minimum free shipping |
| is\_disabled | bit | 1 |  |  | 0 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| email | varchar | 255 |  √  |  | null |  |
| slug | varchar | 511 |  √  |  | null |  |
| type | varchar | 255 |  √  |  | online |  |
| is\_digital | bit | 1 |  |  | false |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| country\_id | Performance | Asc |   |
| id \+ country\_id | Performance | Asc/Asc |   |
| is\_disabled \+ country\_id \+ id | Performance | Asc/Asc/Asc |   |
| is\_disabled \+ is\_deleted \+ id | Performance | Asc/Asc/Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## store\_area {#store_area}

*TBD*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| store\_id | int | 10 |  |  |  | FK(store) |
| country\_id | int | 10 |  √  |  | null | FK(country) |
| area\_id | int | 10 |  |  |  | FK(area) |
| cost | decimal | 10,3 |  |  | 0.000 |  |
| is\_disabled | bit | 1 |  |  | 1 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| delivery\_days | int | 10 |  √  |  | null |  |
| delivery\_time | time | 8 |  √  |  | null |  |
| free\_shipping | decimal | 10,3 |  √  |  | null |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| country\_id \+ area\_id | Must be unique | Asc/Asc |
| area\_id \+ is\_disabled \+ store\_id | Performance | Asc/Asc/Asc |
| store\_id \+ area\_id | Must be unique | Asc/Asc |

## store\_wrapping {#store_wrapping}

*This table stores wrapping types that each warehouse (store) provides.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| store\_id | int | 10 |  |  |  | FK(store) |
| wrapping\_id | int | 10 |  |  |  | FK(wrapping) |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| score | int | 10 |  |  | 100 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| store\_id \+ wrapping\_id | Must be unique | Asc/Asc |

## subcategory {#subcategory}

*This table stores global product subcategory information*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| category\_id | int | 10 |  |  |  | FK(category) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| slug | varchar | 511 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| category\_id | Performance | Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## suggestiongroup   {#suggestiongroup}

*This table is used to create sku suggestion scoped by country*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| name | varchar | 191 |  |  |  |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| country\_id | int | 10 |  |  |  | FK(country) |
| is\_disabled | bit | 1 |  |  | 1 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| country\_id \+ is\_disabled \+ is\_deleted | Performance | Asc/Asc/Asc |

## suggestiongroup\_sku {#suggestiongroup_sku}

*This able is used to associate suggestiongroup with sku*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| suggestionGroup\_id | int | 10 |  |  |  | FK(suggestionGroup) |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| suggestionGroup\_id \+ sku\_id | Performance | Asc/Asc |

## supplier {#supplier}

*This table stores information about a supplier per country. If there is a multinational supplier, they will be duplicated per country e.g. Lego Kuwait, Lego KSA.* 

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| phone | varchar | 31 |  √  |  | null |  |
| is\_disabled | bit | 1 |  |  | 0 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| hold\_date | datetime | 23 |  √  |  | null |  |
| is\_hold | bit | 1 |  |  | 0 |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## supplier\_sku {#supplier_sku}

*This table is used to keep track of supplier sku price*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| supplier\_id | int | 10 |  |  |  | FK(supplier) |
| sku\_id | int | 10 |  |  |  | FK(sku) |
| cost | decimal | 10,3 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| supplier\_id \+ sku\_id | Must be unique | Asc/Asc |

## suppliercontact {#suppliercontact}

*This table stores suppliers’ contact persons’ information*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| supplier\_id | int | 10 |  |  |  | FK(supplier) |
| name | varchar | 255 |  |  |  |  |
| phone | varchar | 31 |  |  |  |  |
| email | varchar | 255 |  |  |  |  |
| position | varchar | 255 |  |  |  |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| supplier\_id \+ email | Must be unique | Asc/Asc |

## tag {#tag}

*This table stores global tag information*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| slug | varchar | 511 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| is\_deleted \+ id | Performance | Asc/Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## tag\_product {#tag_product}

*This table stores global products tags’ information.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| tag\_id | int | 10 |  |  |  | PK, FK(tag) |
| product\_id | int | 10 |  |  |  | PK, FK(product) |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| tag\_id \+ product\_id | Primary key | Asc/Asc |
| product\_id | Performance | Asc |

##  

## tag\_product\_pending {#tag_product_pending}

This table stores pending tag review requests for products.

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | ----- | :---- | :---- | :---- | :---- |
| id | int | 10 |  | √ |  | PK |
| product\_id | int | 10 |  |  |  | FK(product) |
| tag\_id | int | 10 |  |  |  | FK(tag) |
| status | varchar | 191 |  |  | pending' |  |
| requested\_by | int | 10 |  |  |  | FK(admin) |
| requested\_at | timestamp | 3 |  |  | CURRENT\_TIMESTAMP(3) |  |
| reviewed\_by | int | 10 | √ |  | NULL | FK(admin) |
| reviewed\_at | timestamp | 3 | √ |  | NULL |  |
| CDATE | timestamp | 0 |  |  | CURRENT\_TIMESTAMP(0) |  |

| Column(s) | Type | Sort |
| :---- | :---- | :---- |
| id | Primary key | Asc |
| product\_id | Performance | Asc |
| tag\_id | Performance | Asc |
| requested\_by | Performance | Asc |
| reviewed\_by | Performance | Asc |
| status | Performance | Asc |

## taxgroup {#taxgroup}

*TBC*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| title | varchar | 255 |  |  |  |  |
| tax\_amount | decimal | 10,2 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| country\_id | int | 10 |  |  |  | FK(country) |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## taxgroup\_item {#taxgroup_item}

*TBC*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| item | varchar | 191 |  |  |  | “category” |
| item\_id | int | 10 |  |  |  |  |
| taxgroup\_id | int | 10 |  |  |  |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## timeslot ☠️ {#timeslot-☠️}

*Unused*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| deliverymethod\_id | int | 10 |  |  |  | FK(deliverymethod) |
| startDate | timestamp | 19 |  |  |  |  |
| endDate | timestamp | 19 |  |  |  |  |
| closeDate | timestamp | 19 |  |  |  |  |
| capacity | int | 10 |  |  |  |  |
| costDifference | decimal | 10,3 |  |  | 0.000 |  |
| is\_disabled | bit | 1 |  |  | 1 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## tmp\_badge\_migrate {#tmp_badge_migrate}

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| product\_id | int | 10 |  |  |  | FK(product) |
| badge\_id | int | 10 |  |  |  | FK(badge) |
| country\_id | int | 10 |  |  |  | FK(country) |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |

## transaction {#transaction}

*3rd. This table is used for?*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| provider | varchar | 63 |  √  |  | null |  |
| paymentmethod\_id | int | 10 |  |  |  | FK(paymentmethod) |
| invoice\_id | int | 10 |  √  |  | null | FK(invoice) |
| pay | decimal | 10,3 |  |  |  |  |
| fee | decimal | 10,3 |  |  | 0.000 | Payment provider charge |
| hash | varchar | 128 |  |  |  | Used for callback |
| initJson | json | 1073741824 |  √  |  | null |  |
| updateJson | json | 1073741824 |  √  |  | null |  |
| status | bit | 1 |  |  | 0 | 0 \= not paid , 1 \= aid |
| providerId | varchar | 127 |  √  |  | null |  |
| url | varchar | 1024 |  √  |  | null |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| device\_id | int | 10 |  √  |  | null |  |
| user\_id | int | 10 |  √  |  | null |  |
| initReqJson | json | 1073741824 |  √  |  | null |  |
| initResJson | json | 1073741824 |  √  |  | null |  |
| intent | varchar | 63 |  √  |  | null | “order” , “retry”, “giftcard”, “wallet” |
| initRefundJson | json | 1073741824 |  √  |  | null |  |
| refundJson | json | 1073741824 |  √  |  | null |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| hash | Must be unique | Asc |
| invoice\_id \+ id | Performance | Asc/Desc |

## user {#user}

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Host | char | 255 |  |  |  |  |
| has\_alias | bit | 1 |  |  | 0 |  |
| name | varchar | 255 |  √  |  | null |  |
| email | varchar | 300 |  |  |  |  |
| Update\_priv | enum | 1 |  |  | N |  |
| phone | varchar | 63 |  √  |  | null |  |
| password | varchar | 255 |  √  |  | null |  |
| Drop\_priv | enum | 1 |  |  | N |  |
| Reload\_priv | enum | 1 |  |  | N |  |
| status | bit | 1 |  |  | 1 |  |
| Process\_priv | enum | 1 |  |  | N |  |
| lastlogin | timestamp | 19 |  √  |  | null |  |
| Grant\_priv | enum | 1 |  |  | N |  |
| CDate | timestamp | 19 |  √  |  | CURRENT\_TIMESTAMP |  |
| Index\_priv | enum | 1 |  |  | N |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| Show\_db\_priv | enum | 1 |  |  | N |  |
| google\_user\_id | varchar | 255 |  √  |  | null |  |
| business\_email | varchar | 300 |  √  |  | null |  |
| business\_name | varchar | 255 |  √  |  | null |  |
| referral\_code | varchar | 20 |  √  |  | null |  |
| referral\_by | int | 10 |  √  |  | null |  |
| Repl\_client\_priv | enum | 1 |  |  | N |  |
| Create\_view\_priv | enum | 1 |  |  | N |  |
| nzloyalty\_id | varchar | 255 |  √  |  | null |  |
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
| authentication\_string | text | 65535 |  √  |  | null |  |
| password\_expired | enum | 1 |  |  | N |  |
| password\_last\_changed | timestamp | 19 |  √  |  | null |  |
| password\_lifetime | smallint unsigned | 5 |  √  |  | null |  |
| account\_locked | enum | 1 |  |  | N |  |
| Create\_role\_priv | enum | 1 |  |  | N |  |
| Drop\_role\_priv | enum | 1 |  |  | N |  |
| Password\_reuse\_history | smallint unsigned | 5 |  √  |  | null |  |
| Password\_reuse\_time | smallint unsigned | 5 |  √  |  | null |  |
| Password\_require\_current | enum | 1 |  √  |  | null |  |
| User\_attributes | json | 1073741824 |  √  |  | null |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id \+ Host \+ User | Primary key | Asc/Asc/Asc |
| email | Must be unique | Asc |
| is\_deleted | Performance | Asc |

## userList ☠️ {#userlist-☠️}

*Unused. Supposed to be a wishlist.*

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| type | varchar | 255 |  |  |  |  |
| target | varchar | 255 |  |  |  |  |
| user\_id | int | 10 |  |  |  | FK(user) |
| target\_id | int | 10 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| target\_id \+ target \+ user\_id \+ type | Must be unique | Asc/Asc/Asc/Asc |

## userMarklist {#usermarklist}

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| name | varchar | 255 |  |  |  |  |
| user\_id | int | 10 |  |  |  | FK(user) |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| slug | varchar | 511 |  |  |  |  |
| userMarklist\_id | int | 10 |  √  |  | null |  |
| description | varchar | 1023 |  √  |  | null |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| slug \+ is\_deleted | Performance | Asc/Asc |
| slug | Must be unique | Asc |

## userMarklist\_target {#usermarklist_target}

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| userMarklist\_id | int | 10 |  |  |  |  |
| target | varchar | 255 |  |  |  |  |
| target\_id | int | 10 |  |  |  |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| userMarklist\_id \+ target \+ target\_id | Primary key | Asc/Asc/Asc |

## wallettransaction {#wallettransaction}

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| user\_id | int | 10 |  |  |  | FK(user) |
| admin\_id | int | 10 |  √  |  | null | FK(admin) |
| refundable | bit | 1 |  |  | 1 | Not other value other than 1 ( |
| amount | decimal | 10,3 |  |  |  | Can be positive and negative |
| transaction\_id | int | 10 |  √  |  | null |  |
| target | varchar | 31 |  √  |  | null | creditnote giftcard invoice referralUser “Debutnote”, “referralUser” \- turneedoff  |
| target\_id | int | 10 |  √  |  | null |  |
| status | tinyint | 3 |  √  |  | 0 | 0 \= Invalid/Cancelled, 1Valid |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| detailJson | json | 1073741824 |  √  |  | null | Only used by referral to store  |
| is\_digital\_gift | varchar | 255 |  |  |  | Virtual column  If target \= digital\_gift: is\_digital\_gift \=  user\_id\_target\_id\_target Else is\_digital\_gift \= null  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| transaction\_id | Must be unique | Asc | This unique column is also nullable |
| user\_id \+ target\_id \+ target | Must be unique if target \= digital\_gift |  | Partial index if target \= digital\_gift |

## websiteMenuItem ☠️ {#websitemenuitem-☠️}

Unused at the moment. Dynamic menu per country.

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  √  |  | null | FK(country) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| type | varchar | 50 |  |  |  |  |
| target | json | 1073741824 |  √  |  | null |  |
| url | varchar | 2047 |  √  |  | null |  |
| displayorder | int | 10 |  |  | 999 |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| slug | varchar | 511 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## Widget {#widget}

Use for home page widget

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| country\_id | int | 10 |  |  |  | FK(country) |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| type | varchar | 63 |  |  |  |  |
| target | json | 1073741824 |  √  |  | null |  |
| url | varchar | 1023 |  √  |  | null |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| slug | varchar | 511 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## wrapping {#wrapping}

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| name\_en | varchar | 255 |  |  |  |  |
| name\_ar | varchar | 255 |  |  |  |  |
| is\_deleted | bit | 1 |  |  | 0 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |
| slug | varchar | 511 |  √  |  | null |  |

| Column(s) | Type | Sort | Anomalies |
| ----- | ----- | ----- | ----- |
| id | Primary key | Asc |   |
| slug | Must be unique | Asc | This unique column is also nullable |

## wrapping\_country {#wrapping_country}

| Name | Type | Size | Null? | Auto | Default | Comment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| id | int | 10 |  |  √  |  | PK |
| wrapping\_id | int | 10 |  |  |  | FK(wrapping) |
| country\_id | int | 10 |  |  |  | FK(country) |
| price | decimal | 10,3 |  |  |  |  |
| old\_price | decimal | 10,3 |  √  |  | null |  |
| is\_disabled | bit | 1 |  |  | 1 |  |
| CDate | timestamp | 19 |  |  | CURRENT\_TIMESTAMP |  |
| UDate | datetime | 23 |  |  | CURRENT\_TIMESTAMP(3) |  |

| Column(s) | Type | Sort |
| ----- | ----- | ----- |
| id | Primary key | Asc |
| wrapping\_id \+ country\_id | Must be unique | Asc/Asc |

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA10AAAAUCAYAAAB2xFdmAAABU0lEQVR4Xu3XMVEFABQDwS8LB6hAACVecIASFFCjABPMQB8HydtiPdw9vj7f/9j38fMN037fnoAxry/PABMeGedsykCFNRlrQL+MFoBWpuuIDFRYk7EG9MtoAWhluo7IQIU1GWtAv4wWgFam64gMVFiTsQb0y2gBaGW6jshAhTUZa0C/jBaAVqbriAxUWJOxBvTLaAFoZbqOyECFNRlrQL+MFoBWpuuIDFRYk7EG9MtoAWhluo7IQIU1GWtAv4wWgFam64gMVFiTsQb0y2gBaGW6jshAhTUZa0C/jBaAVqbriAxUWJOxBvTLaAFoZbqOyECFNRlrQL+MFoBWpuuIDFRYk7EG9MtoAWhluo7IQIU1GWtAv4wWgFam64gMVFiTsQb0y2gBaGW6jshAhTUZa0C/jBaAVqbriAxUWJOxBvTLaAFoZbqOyECFNRlrQL+MFoBW/2g81Q+I7aaDAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,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>

[image3]: <data:image/png;base64,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>

[image4]: <data:image/png;base64,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>

[image5]: <data:image/png;base64,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>