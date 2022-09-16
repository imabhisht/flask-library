
# Portfolio

My Portfolio: https://www.imbhisht.com

## References

Based on Scouto (acquired By Spinny) Assignment Questions.

## API Reference

#### Get all information about book

```http
  GET /book
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `query` | `array` | **Required**. Ex: /book?query=[pepissued, pepcurrent]&bookName=${bookname} |
|           |       | where pepissued = List of User who Issued book.|
|           |       | where pepcurrent = List of User who Currently Issue book.    
|   `bookName`  | `string`      |  Name of the Book     | where pepissued = List of User who Issued book.|

#### Get all information about person


```http
  GET /person
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `query` | `array` | **Required**. Ex: /person?query=[current, returned, issued]&bookName=${bookname} |
|           |       | where current = List of Books user currently Issued. |
|           |       | where returned = List of Books user returned.    
|   `personName`  | `string`      |  Name of the User     | where pepissued = List of User who Issued book.

#### Get Books Information & Search Features

```http
  GET /books?name=india
  GET /books?name=kore&category=adventure   
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`      | `string` | Name of the book |
| ` category`      | `string` |  Category of book to fetch |
| `rent`      | `integer` |  Rent for Sorting |
| `rentMin`      | `integer` |  Min Rent for Sorting |
| `rentMin`      | `integer` |  Max Rent for Sorting |

#### Get Books Issue for User

```http
  GET /book/issue?bookName=india&personName=rahul
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `bookName`      | `string` | Name of the book |
| ` personName`      | `string` |  Name of the Person |


#### Get Books Returned for User

```http
  GET /book/return?bookName=india&personName=rahul
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `bookName`      | `string` | Name of the book |
| ` personName`      | `string` |  Name of the Person |



  