$(function () {

    window.Profile = Backbone.Model.extend({
        urlRoot: PROFILE_API_URL
    });
 
    window.ProfileCollection = Backbone.Collection.extend({
        model: Profile,
        urlRoot: PROFILE_API_URL
    });

    window.ProfileView = Backbone.View.extend({
        tagname: "div",
        className: "profileExpanded",
        
        events: {
            "change .profileAttribute" : "updateModelFromView",
            "click .saveProfileButton": "saveProfile"
        },

        initialize: function () {
            _.bindAll(this, "updateModelFromView", "saveProfile", "updateModelField");
        },

        render: function () {
            $(this.el).html(ich.profileTemplate(this.model.toJSON()));
            return this;
        },

        updateModelField: function (model, el) {
            if (el.attr('profileFieldName').indexOf("user.") == 0) { 
                var fieldName = el.attr('profileFieldName').replace("user.", "");
                var user = model.get("user");
                if (!user) {
                    user = {};
                }
                user[fieldName] = this.valueFromElement(el);
                model.set("user", user);
            } else {
                model.set(el.attr('profileFieldName'), this.valueFromElement(el));
            }
        },

        updateModelFromView: function () {
            var me = this;
            this.$('.profileAttribute').each(function () {
                me.updateModelField(me.model, $(this));
            });
        },

        valueFromElement: function (el) {
            if (el.type == 'checkbox') {
                return el.is(':checked');
            }

            return el.val();
        },

        saveProfile: function () {
            this.model.save();
        }
    });

    window.ProfileThumbView = Backbone.View.extend({
        tagName: "li",

        events: {
            "click .profileHeader" : "toggleProfileView"
        },

        initialize: function () {
            _.bindAll(this, "render", "toggleProfileView");
            this.model.on('change', this.render, this);
        },

        render: function () { 
            $(this.el).html(ich.profileThumbTemplate(this.model.toJSON()));

            if (this.expanded) {                      
                var expandedView = new ProfileView({ model : this.model });
                this.$(".profileExpanded").html(expandedView.render().el);
            } else {
                this.$(".profileExpanded").hide("");               
            }

            return this;
        },
        
        toggleProfileView: function () {
            this.expanded = !this.expanded;
            return this.render();
        },
	
	expanded: false
    });

    window.CreateProfileView = Backbone.View.extend({
        el: "#profile",

        initialize: function () {
	    _.bindAll(this, "registerListView", "addToCollectionAndReset");
            this.profile = new Profile();
            var view = new ProfileView({ model : this.profile });
            $(this.el).append(view.render().el);
        },
        
        registerListView: function(profileListView) {
            this.profileListView = profileListView;
            this.profile.on("change:id", this.addToCollectionAndReset);
        },
        
        addToCollectionAndReset: function () {
            if (this.profileListView) {
                this.profileListView.profiles.add(this.profile);
            }
            this.profile = new Profile();
            this.profile.on("change:id", this.addToCollectionAndReset);
            var view = new ProfileView({ model : this.profile });
            $(this.el).html(view.render().el);
        }
    });

    window.ProfileListView = Backbone.View.extend({
        el: "#profileList", 

        initialize: function () { 
            _.bindAll(this, "addOne", "addAll");
            
            this.profiles = new ProfileCollection();
            this.profiles.bind("add", this.addOne);
            this.profiles.bind("reset", this.addAll);
            this.profiles.fetch();
        },
         
        addOne: function (profile) { 
            var view = new ProfileThumbView({ model : profile }); 
            $(this.el).append(view.render().el); 
        }, 
 
        addAll: function () { 
           this.profiles.each(this.addOne); 
        },
    });
    
    window.createProfileView = new CreateProfileView();
    window.profileListView = new ProfileListView();
    window.createProfileView.registerListView(window.profileListView);
});
