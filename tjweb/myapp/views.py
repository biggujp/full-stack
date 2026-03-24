from pydoc import html
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
html =  '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Hello World</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

  <!-- Google Font -->
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap" rel="stylesheet">

  <style>
    body {
      font-family: 'Poppins', sans-serif;
      height: 100vh;
      margin: 0;
      background: linear-gradient(135deg, #667eea, #764ba2);
      display: flex;
      justify-content: center;
      align-items: center;
      color: white;
    }

    .card {
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border: none;
      border-radius: 20px;
      padding: 40px;
      text-align: center;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
      animation: fadeIn 1.5s ease;
    }

    h1 {
      font-size: 3rem;
      font-weight: 600;
      margin-bottom: 10px;
    }

    p {
      opacity: 0.8;
    }

    .btn-custom {
      margin-top: 20px;
      border-radius: 50px;
      padding: 10px 25px;
      background: white;
      color: #764ba2;
      border: none;
      transition: 0.3s;
    }

    .btn-custom:hover {
      background: #f1f1f1;
      transform: scale(1.05);
    }

    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: translateY(30px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
  </style>
</head>
<body>

  <div class="card">
    <h1>Hello, World 👋</h1>
    <p>Welcome to your beautiful Bootstrap page</p>
    <button class="btn btn-custom" onclick="showAlert()">Click Me</button>
  </div>

  <!-- Bootstrap JS -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

  <script>
    function showAlert() {
      alert("Hello from your stylish page! 😎");
    }
  </script>

</body>
</html>
'''

def Home(request):    
    return HttpResponse(html)