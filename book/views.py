from operator import truediv
from urllib import request
from django.db import connection
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def book_list(request):
    with connection.cursor() as cursor:
        genre = request.query_params.get('genre')
        cursor.execute("SELECT * from book_book WHERE (genre = %s or (genre = %s) is NULL)", [genre, genre])
        books = dictfetchall(cursor)

    return Response(books)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
    try: 
        with connection.cursor() as cursor:
            user_id = request.user.id
            book_id = request.data.get('book_id')
            rating = request.data.get('rating')
            
            if not book_availability(book_id):
                return Response("Book with given id does not exist.", status=status.HTTP_400_BAD_REQUEST)
                
            cursor.execute("INSERT INTO book_review (user_id, book_id, rating) VALUES(%s, %s, %s)", [user_id, book_id, rating])
    except IntegrityError as ex:
        if ex.__cause__.diag.constraint_name == "rating_check":
            return Response("The rating must be between 1 and 5.", status=status.HTTP_400_BAD_REQUEST)
        return Response("You have already rated the book with given id.", status=status.HTTP_400_BAD_REQUEST)


    return Response({"book_id": book_id, "rating": rating}, status=status.HTTP_201_CREATED)
        

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_review(request):
    with connection.cursor() as cursor:
        user_id = request.user.id
        book_id = request.data.get('book_id')
        rating = request.data.get('rating')
        
        if not existing_rating(book_id, user_id):
            return Response("No rating is available for the book with given id.", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cursor.execute("UPDATE book_review SET rating = %s WHERE book_id = %s AND user_id = %s", [rating, book_id, user_id])
        except IntegrityError as ex:
            if ex.__cause__.diag.constraint_name == "rating_check":
                return Response("The rating must be between 1 and 5.", status=status.HTTP_400_BAD_REQUEST)
        
    return Response({"book_id": book_id, "rating": rating})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request):
    with connection.cursor() as cursor:
        user_id = request.user.id
        book_id = request.data.get('book_id')
        
        if not existing_rating(book_id, user_id):
            return Response("No rating is available for the book with given id.", status=status.HTTP_400_BAD_REQUEST)
        
        cursor.execute("DELETE FROM book_review WHERE book_id = %s AND user_id = %s", [book_id, user_id])

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def suggest_book(request):
    with connection.cursor() as cursor:
        user_id = request.user.id
        cursor.execute("SELECT genre, ROUND(AVG(rating), 2) average_rating from book_book B JOIN book_review R ON B.id = R.book_id WHERE user_id = %s  GROUP BY genre ORDER BY average_rating DESC LIMIT 1", [user_id])
        
        if cursor.rowcount:
            genres = dictfetchall(cursor)
            favorite_genre = genres[0].get('genre', None)
            cursor.execute("SELECT B.id, B.title, B.author from book_book B LEFT OUTER JOIN book_review R ON B.id = R.book_id WHERE genre = %s AND R.user_id IS NULL", [favorite_genre])
            suggested_books = dictfetchall(cursor)
            if cursor.rowcount:
                return Response(suggested_books)
            
            return Response(f"Great, You have already read all books in your favorite genre ({favorite_genre})!", status=status.HTTP_204_NO_CONTENT)
                
        
        return Response("Sorry, There is not enough data about you.", status=status.HTTP_204_NO_CONTENT)


def book_availability(book_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id from book_book WHERE id = %s", [book_id])
        if cursor.rowcount:
            return True
        
    return False


def existing_rating(book_id, user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id from book_review WHERE book_id = %s AND user_id = %s", [book_id, user_id])
        if cursor.rowcount:
            return True
        
    return False


def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]