from flask import request
from flask_restful import Resource
import uuid
from app.models import books_db

class BookList(Resource):
    def get(self):
        """
        Отримати список всіх книг
        ---
        tags:
          - Books
        responses:
          200:
            description: Успішно отримано список книг
        """
        return books_db, 200

    def post(self):
        """
        Додати нову книгу
        ---
        tags:
          - Books
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - title
                - author
                - year
              properties:
                title:
                  type: string
                  example: "Кобзар"
                author:
                  type: string
                  example: "Тарас Шевченко"
                year:
                  type: integer
                  example: 1840
                status:
                  type: string
                  example: "наявна в бібліотеці"
        responses:
          201:
            description: Книга успішно створена
        """
        data = request.get_json()
        new_book = {
            "id": str(uuid.uuid4()),
            "title": data.get("title"),
            "author": data.get("author"),
            "year": data.get("year"),
            "status": data.get("status", "наявна в бібліотеці")
        }
        books_db.append(new_book)
        return new_book, 201

class BookResource(Resource):
    def get(self, book_id):
        """
        Отримати книгу за ID
        ---
        tags:
          - Books
        parameters:
          - in: path
            name: book_id
            type: string
            required: true
            description: ID книги (UUID)
        responses:
          200:
            description: Дані книги
          404:
            description: Книгу не знайдено
        """
        book = next((b for b in books_db if b["id"] == book_id), None)
        if book:
            return book, 200
        return {"message": "Book not found"}, 404

    def delete(self, book_id):
        """
        Видалити книгу за ID
        ---
        tags:
          - Books
        parameters:
          - in: path
            name: book_id
            type: string
            required: true
            description: ID книги (UUID)
        responses:
          204:
            description: Книгу успішно видалено
        """
        global books_db
        books_db[:] = [b for b in books_db if b.get("id") != book_id]
        return '', 204