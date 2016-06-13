app.module("TopicsByChannel", function (TopicsByChannel, NewsChallengeApp, Backbone, Marionette, $, _) {
    var ChannelModel = Backbone.Model.extend({
        defaults: {
            name: null,
            topics: []
        }
    });

    var ChannelCollection = Backbone.Collection.extend({
        model: ChannelModel,
        url: function () {
            return NewsChallengeApp.newsApiUrl + '/topic/best_by_channel';
        }
    });

    var NoChildrenView = Marionette.ItemView.extend({
        template: '#empty-template',
        className: 'col-xs-12'
    });

    var ChannelView = Marionette.ItemView.extend({
        template: '#channel-template',
        className: 'col-xs-12 col-md-6'
    });

    var ChannelCollectionView = Marionette.CompositeView.extend({
        collection: ChannelCollection,
        childView: ChannelView,
        emptyView: NoChildrenView,
        template: '#composite-view-template',
        childViewContainer: '#channels-collection',
        ui: {
            submitButton: 'button[type="submit"]',
            topicDateInput: '#topic-date',
            topicName: '#topic-date-group'
        },
        events: {
            'click @ui.submitButton': 'onSubmitButtonClick'
        },

        onSubmitButtonClick: function (event) {
            event.preventDefault();
            var topicDate = new Date(this.ui.topicDateInput.val());
            var today = new Date();
            var utcTopicDate = new Date(Date.UTC(topicDate.getUTCFullYear(), topicDate.getUTCMonth(), topicDate.getUTCDate()));
            var utcToday = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate()));

            if (utcTopicDate < utcToday) {
                $(this.childViewContainer).addClass('hidden-xs-up');
                this.ui.submitButton.addClass('active');
                this.ui.topicName.removeClass('has-danger');
                
                var view = this;
                this.collection.fetch({
                    complete: function () {
                        view.ui.submitButton.removeClass('active');
                        $(view.childViewContainer).removeClass('hidden-xs-up');
                    },
                    data: {
                        date: view.ui.topicDateInput.val()
                    }
                });
            } else {
                $(this.childViewContainer).addClass('hidden-xs-up');
                this.ui.topicName.addClass('has-danger');
            }
        }
    });

    var ChannelLayoutView = Marionette.LayoutView.extend({
        template: false,
        el: 'topic-by-channel-view',
        regions: {
            collectionRegion: '#collection'
        },
        onRender: function () {
            this.collectionRegion.show(new ChannelCollectionView({collection: new ChannelCollection()}));
        }
    });

    TopicsByChannel.currentView = new ChannelLayoutView();
    TopicsByChannel.currentView.render();
});