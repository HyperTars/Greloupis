# Database Design

| Database                | Table / Collection | Data / Document        |        |                 |        |                |      | Description |
|-------------------------|--------------------|------------------------|--------|-----------------|--------|----------------|------|-------------|
|                         |                    | Attr                   | Type   | Sub\-Attr       | Type   | Sub\-Sub\-Attr | Type |             |
| online\_video\_platform | user               | user\_id               |        |                 |        |                |      |             |
|                         |                    | user\_email            |        |                 |        |                |      |             |
|                         |                    | user\_name             |        |                 |        |                |      |             |
|                         |                    | user\_password         |        |                 |        |                |      |             |
|                         |                    | user\_detail           | Object | first\_name     |        |                |      |             |
|                         |                    |                        |        | last\_name      |        |                |      |             |
|                         |                    |                        |        | phone           |        |                |      |             |
|                         |                    |                        |        | address         | Object | street1        |      |             |
|                         |                    |                        |        |                 |        | street2        |      |             |
|                         |                    |                        |        |                 |        | city           |      |             |
|                         |                    |                        |        |                 |        | state          |      |             |
|                         |                    |                        |        |                 |        | country        |      |             |
|                         |                    |                        |        |                 |        | zip            |      |             |
|                         |                    | user\_status           |        |                 |        |                |      |             |
|                         |                    | user\_thumbnail        | Object | thumbnail\_uri  |        |                |      |             |
|                         |                    |                        |        | thumbnail\_type |        |                |      |             |
|                         |                    | user\_follower         |        |                 |        |                |      |             |
|                         |                    | user\_reg\_date        |        |                 |        |                |      |             |
|                         |                    | user\_recent\_login    | Array  | login\_ip       |        |                |      |             |
|                         |                    |                        |        | login\_time     |        |                |      |             |
|                         | follow             | follow\_uploader       |        |                 |        |                |      |             |
|                         |                    | follow\_by             |        |                 |        |                |      |             |
|                         |                    | follow\_date           |        |                 |        |                |      |             |
|                         | history            | history\_id            |        |                 |        |                |      |             |
|                         |                    | user\_id               |        |                 |        |                |      |             |
|                         |                    | video\_id              |        |                 |        |                |      |             |
|                         |                    | process                |        |                 |        |                |      |             |
|                         |                    | history\_date          |        |                 |        |                |      |             |
|                         | video              | video\_id              |        |                 |        |                |      |             |
|                         |                    | user\_id               |        |                 |        |                |      |             |
|                         |                    | video\_title           |        |                 |        |                |      |             |
|                         |                    | video\_tag             | Array  |                 |        |                |      |             |
|                         |                    | video\_category        | Array  |                 |        |                |      |             |
|                         |                    | video\_description     |        |                 |        |                |      |             |
|                         |                    | video\_language        |        |                 |        |                |      |             |
|                         |                    | video\_status          |        |                 |        |                |      |             |
|                         |                    | video\_content         |        |                 |        |                |      |             |
|                         |                    | video\_content\_status |        |                 |        |                |      |             |
|                         |                    | video\_size            |        |                 |        |                |      |             |
|                         |                    | video\_view            |        |                 |        |                |      |             |
|                         |                    | video\_like            |        |                 |        |                |      |             |
|                         |                    | video\_dislike         |        |                 |        |                |      |             |
|                         |                    | video\_comment         |        |                 |        |                |      |             |
|                         |                    | video\_star            |        |                 |        |                |      |             |
|                         |                    | video\_share           |        |                 |        |                |      |             |
|                         |                    | video\_thumbnail       | Object | thumbnail\_uri  |        |                |      |             |
|                         |                    |                        |        | thumbnail\_type |        |                |      |             |
|                         |                    | video\_upload\_date    |        |                 |        |                |      |             |
|                         |                    | video\_uri             | Object | video\_low      |        |                |      |             |
|                         |                    |                        |        | video\_mid      |        |                |      |             |
|                         |                    |                        |        | video\_high     |        |                |      |             |
|                         | comment            | comment\_id            |        |                 |        |                |      |             |
|                         |                    | user\_id               |        |                 |        |                |      |             |
|                         |                    | video\_id              |        |                 |        |                |      |             |
|                         |                    | comment                |        |                 |        |                |      |             |
|                         |                    | comment\_date          |        |                 |        |                |      |             |
|                         | like               | like\_id               |        |                 |        |                |      |             |
|                         |                    | user\_id               |        |                 |        |                |      |             |
|                         |                    | video\_id              |        |                 |        |                |      |             |
|                         |                    | like\_date             |        |                 |        |                |      |             |
|                         | dislike            | dislike\_id            |        |                 |        |                |      |             |
|                         |                    | user\_id               |        |                 |        |                |      |             |
|                         |                    | video\_id              |        |                 |        |                |      |             |
|                         |                    | dislike\_date          |        |                 |        |                |      |             |
|                         | star               | star\_id               |        |                 |        |                |      |             |
|                         |                    | user\_id               |        |                 |        |                |      |             |
|                         |                    | video\_id              |        |                 |        |                |      |             |
|                         |                    | star\_date             |        |                 |        |                |      |             |
