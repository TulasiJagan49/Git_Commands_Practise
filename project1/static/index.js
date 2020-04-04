// console.log("In JS file")
function search() {
    // console.log("inside search function")
    var xhr = new XMLHttpRequest();
    var search_query = document.getElementById("book").value;
    // console.log(search_query)
    xhr.open("POST", "/api/search/");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // console.log(JSON.stringify({ "query": search_query}))
    xhr.send(JSON.stringify({ "query": search_query}));
    xhr.onload = function () {
        // console.log("inside search")
        if (xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            console.log(data)
            var json_array = data["books"];
            var content = '<thead class="thead-light"><tr><th>Results:</th></tr></thead>';
            for (x in json_array) {
                content += '<tr> <th scope="row"> <a href="#" onclick=book("'+ json_array[x]["isbn"] + '")>' + json_array[x]["title"] +'</a> </th> </tr>';
            }
            document.querySelector("#result").innerHTML = content;
        } else {
            document.querySelector("#result").innerHTML = "Invalid ISBN Number";
        }
    };
}


function book(isbn) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/book/'+isbn);
    xhr.onload = function() {
        if (xhr.status === 200) {
            let s = JSON.parse(xhr.responseText);
            console.log(s)
            var content = '<thead class="thead-light"><tr><th scope="col" colspan=2>Details:</th></tr></thead>';
            content += '<tr> <td scope="row">ISBN Number</td><td>' + s.ISBN + '</td></tr>' +
                            '<tr> <td scope="row">Title</td><td>' + s.Title + '</td></tr>' +
                            '<tr> <td scope="row">Auhtor</td><td>' + s.Author + '</td></tr>' +
                            '<tr> <td scope="row">Year</td><td>' + s.year + '</td></tr>'

            document.querySelector("#details").innerHTML = content;
        }
        else {
            document.querySelector("#details").innerHTML = "Invalid ISBN Number";
        }
    };
    xhr.send();
  }