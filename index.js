
const express = require('express')
const path = require('path')
const fs = require('fs')
const { PythonShell } = require('python-shell')
const app = express()
const port = 3000



app.use(express.json())

app.post('/', async (req, res) => {
  
  
  const json =  JSON.stringify(req.body)

  console.log(json)

    Options = {

    scriptPath : '/root/server',

    args: [

      json

    ]

   }

  await PythonShell.run('generatecert.py',Options).then((message) => {
    
    console.log(message)
    if(message.includes("error")){
     
      res.sendStatus(500)
    }else {
      res.sendStatus(200).send("OK");
    }

    
  }).catch((reson) => {

    res.status(500).send("Error");
  })


})


app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})