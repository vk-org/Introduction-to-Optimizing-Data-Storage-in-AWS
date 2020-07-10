var ViewModel = function () {
  var self = this;

  self.url = window.location.href
  self.existingImages = ko.observableArray([]);
  
  self.updateImages = function () {
    $.getJSON(self.url+'listmedia', function (data) {
      self.existingImages.removeAll();
      for (i = 0; i < data.length; i++) {
        if (data[i].file_data.substring(0,5) != "https") {
          data[i].file_data = 'data:image/jpg;base64,' + data[i].file_data; 
        } 
        self.existingImages.push(data[i]);
      };
      self.existingImages.sort();
      self.existingImages.reverse();
    });
  };

  self.updateImages();

  self.fileSelect = function (element, event) {
    var files = event.target.files;

    for (var i = 0, f; f = files[i]; i++) {
      var formData = new FormData();

      formData.append("file", f)
      if (!f.type.match('image.*')) {
        continue;
      }

      axios.post(self.url+'upload',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  };
  var imageFresh = window.setInterval(self.updateImages, 3000)
};

var FileModel = function (name, src) {
  var self = this;
  this.name = name;
  this.src = src;
};

ko.applyBindings(new ViewModel());
