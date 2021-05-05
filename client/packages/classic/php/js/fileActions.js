// inspired by https://github.com/PaulLereverend/NextcloudExtract/blob/master/js/extraction.js
(function (OC, window, $, undefined) {
  "use strict";

  OC.rds = OC.rds || {};

  let checkLogin = new Promise((resolve, reject) => {
    let self = { resolve, reject }

    OC.rds.loggedIn = false

    let config = new Promise((resolve, reject) => {
      OC.AppConfig.getValue("rds", "cloudURL", function (response) {
        if (!response) {
          OC.rds.config = {
            url: "http://localhost:8080",
            server: "http://localhost:8080"
          };
          reject("cloudURL is empty")
        } else {
          OC.rds.config = { url: response, server: response }
          resolve({ url: response, server: response })
        }
      })
    })

    config.finally(() => {
      let login = new Promise((resolve, reject) => {
        fetch(`${OC.rds.config.server}/login`, { credentials: "include" })
          .then((response) => {
            if (response.ok) {
              OC.rds.loggedIn = true
              resolve(true)
              self.resolve(true)
            } else {
              reject("user not logged in")
            }
          })
      })

      login.catch(() => {
        $.get(OC.generateUrl("/apps/rds/api/1.0/informations"))
          .done((response) => {
            $.ajax({
              type: "post",
              url: `${OC.rds.config.server}/login`,
              data: { "informations": response.jwt },
              crossDomain: true,
              xhrFields: {
                withCredentials: true
              },
            })
              .done(() => {
                OC.rds.loggedIn = true
                self.resolve(true)
              })
          })
      })
    });
  })

  var folderDict = {};

  const addFolderToResearch = {
    init: function (mimetype, fileActions) {
      var self = this;
      fileActions.registerAction({
        name: "addFolderToResearch",
        displayName: t("upload_zenodo", "Add folder to RDS"),
        mime: mimetype,
        permissions: OC.PERMISSION_UPDATE,
        type: OCA.Files.FileActions.TYPE_DROPDOWN,
        iconClass: "icon-rds-research-small",
        actionHandler: function (filename, context) {
          var fileName = "";
          var mimetype = context.$file.data("mime");
          var dir = context.fileList.getCurrentDirectory();

          if (!dir.endsWith("/")) {
            dir += "/";
          }

          fileName = dir + filename;
          if (mimetype === "httpd/unix-directory") {
            fileName += "/"
          }

          window.location = OC.generateUrl("apps/rds/?createResearch&folder=" + fileName)
        },
      });
    },
  };
  const pushFileToResearch = {
    init: function (mimetype, fileActions) {
      var self = this;
      fileActions.registerAction({
        name: "pushFileToResearch",
        displayName: t("upload_zenodo", "Update RDS file"),
        mime: mimetype,
        permissions: OC.PERMISSION_UPDATE,
        type: OCA.Files.FileActions.TYPE_DROPDOWN,
        iconClass: "icon-rds-research-small",
        actionHandler: function (filename, context) {
          var fileName = "";
          var mimetype = context.$file.data("mime");
          var dir = context.fileList.getCurrentDirectory();

          if (!dir.endsWith("/")) {
            dir += "/";
          }

          fileName = dir + filename;
          if (mimetype === "httpd/unix-directory") {
            fileName += "/"
          }

          var data = {
            filename: fileName,
            researchIndex: folderDict[fileName]
          };

          // TODO Popup a message about status
          //socket.emit("triggerSynchronization", data)
        },
      });
    },
  };
  var createRdsResearch = {
    attach: function (menu) {
      menu.addMenuEntry({
        id: "createRdsResearch",
        displayName: "RDS research project",
        templateName: "templateName.ext",
        iconClass: "icon-rds-research-small",
        fileType: "file",
        actionHandler: function () {
          console.log("go to rds and create a research project");
          // TODO add socket / redirect func for creating a new rds project and redirect the user
          //socket.emit("getAllFiles");
        },
      });
    },
  };

  function addActions(directories) {
    OC.rds.directories = directories
    OC.Plugins.register('OCA.Files.FileList', OC.rds.FilePlugin);
  }



  function attachFilelist(fileList) {
    // add file actions in here using
    var mimes = ["httpd/unix-directory"];
    mimes.forEach((item) => {
      addFolderToResearch.init(item, fileList.fileActions);
    });
    pushFileToResearch.init("all", fileList.fileActions);

    OC.rds.directories = [];

    // setup advanced filter
    fileList.fileActions.addAdvancedFilter(function (actions, context) {
      var fileName = context.$file.data("file");
      var mimetype = context.$file.data("mime");
      var dir = context.fileList.getCurrentDirectory();

      var found = false;
      var researchIndex = undefined;
      for (var key in OC.rds.directories) {
        var item = OC.rds.directories[key];

        // check if following is in folders:
        // - current directory (because then the files can be pushed separately)
        // - one of the files (can be pushed manually)
        // - edge case: filenames in root dir
        if (item === dir + "/" || item === dir + "/" + fileName + "/" || dir === "/" && item == "/" + fileName + "/") {
          found = true;
          researchIndex = key;
          folderDict[item] = researchIndex
        }
      };

      if (found) {
        if (mimetype === "httpd/unix-directory") {
          delete actions.addFolderToResearch;
        }
      } else {
        delete actions.pushFileToResearch;
      }

      return actions;
    });
  }

  OC.rds.FilePlugin = {
    attach: attachFilelist
  }

  OC.rds.setupActions = function () {
    /* Create menu entry */
    OC.Plugins.register("OCA.Files.NewFileMenu", createRdsResearch);

    /* Add actions, when checkLogin is done. */
    checkLogin.then(() => {
      const socket = io(OC.rds.config.server, {
        reconnection: true,
        reconnectionDelay: 3000,
        maxReconnectionAttempts: Infinity,
        transports: ["websocket"],
        withCredentials: true,
        autoConnect: false
      });

      socket.on("connect", () => {
        console.log("connected ws")
        // TODO get all directories from socket with struct {"123":"/asd", "1222":"/mampf"}
        //socket.emit("getAllResearches", addActions);
      });

      socket.open()
    })
  }

  OC.rds.setupActions()
})(OC, window, jQuery);
