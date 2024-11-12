db.collection.find().forEach(function(doc) {
    var parsedValue = JSON.parse(doc.value);  // Parse the 'value' field
    var parsedData = JSON.parse(parsedValue.data);  // Parse the nested 'data' field
    printjson(parsedData.licenseid);  // Print the 'licenseid' value
});
