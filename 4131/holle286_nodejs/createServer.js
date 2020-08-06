const http = require('http');
const url = require('url');
const fs = require('fs');
const qs = require('querystring');

http.createServer(function (req, res) {
  var q = url.parse(req.url, true);
  var filename = "." + q.pathname;
  if(req.url === '/'){
    indexPage(req,res);
  }
  else if(req.url === '/index.html'){
    indexPage(req,res);
  }
  else if(req.url ==='/contact.html'){
    //get file and return contents of contact.json
    contactPage(req,res);
  }
  else if(req.url === '/addContact.html') {
    addContactPage(req,res);
  }
  else if(req.url === '/postContactEntry') {
    handlePost(req,res);
  }
  else if(req.url === '/stock.html') {
    stockPage(req,res);
  }
  else if(req.url === '/contact.json') {
    handleJson(req,res);
  }
  else{
    res.writeHead(404, {'Content-Type': 'text/html'});
    return res.end("404 Not Found");
  }
}).listen(9001);

function contactPage(req, res) {
  fs.readFile('client/contact.html', function(err, html) {
    if(err) {
      throw err;
    }
    res.statusCode = 200;
    res.setHeader('Content-type', 'text/html');
    res.write(html);
    res.end();
  });

}

function handlePost(req, res) {
      res.writeHead(301,{Location:'./contact.html'});
      res.end();
}

function handleJson(req, res) {
  path = './contact.json'
    fs.readFile(path,function (err, data) {
      if(err) {
        throw err;
      }
      //console.log(res);
      res.setHeader('Content-type', 'text/html');
      res.write(data);
      res.end();
  });
}

function addContactPage(req, res) {
  fs.readFile('client/addContact.html', function(err, html) {
    if(err) {
      throw err;
    }
    res.statusCode = 200;
    res.setHeader('Content-type', 'text/html');
    res.write(html);
    res.end();
  });

}

function stockPage(req,res) {
  fs.readFile('client/stock.html', function(err, html) {
    if(err) {
      throw err;
    }
    res.statusCode = 200;
    res.setHeader('Content-type', 'text/html');
    res.write(html);
    res.end();
  });
}

function indexPage(req, res) {
  fs.readFile('client/index.html', function(err, html) {
    if(err) {
      throw err;
    }
    res.statusCode = 200;
    res.setHeader('Content-type', 'text/html');
    res.write(html);
    res.end();
  });
}

//extract information from post request, and put into a string maybe put into json object or make a json object string out of it, extract information
//read in the file content of json, stringify it, add new string concatenated you made from post data, that is a json object string, append to string that was in contacts.json file that you stringified,
// then you have a big string that you write it back out, write update string back out to contact json file, then send back redirect message
