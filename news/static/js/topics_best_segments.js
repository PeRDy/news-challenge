app.module("TopicsPerformance", function (TopicsPerformance, NewsChallengeApp, Backbone, Marionette, $, _) {
    var SegmentModel = Backbone.Model.extend({
        defaults: {
            start: null,
            end: null,
            channel: null
        }
    });

    var SegmentCollection = Backbone.Collection.extend({
        model: SegmentModel,
        url: function () {
            return NewsChallengeApp.newsApiUrl + '/segment/best_segments';
        }
    });

    var NoChildrenView = Marionette.ItemView.extend({
        template: '#empty-template',
        className: 'col-xs-12'
    });

    var SegmentView = Marionette.ItemView.extend({
        template: '#segment-template',
        className: 'col-xs-12 col-md-6'
    });

    var SegmentCollectionView = Marionette.CompositeView.extend({
        collection: SegmentCollection,
        childView: SegmentView,
        emptyView: NoChildrenView,
        template: '#composite-view-template',
        childViewContainer: '#segments-collection',
        ui: {
            submitButton: 'button[type="submit"]',
            topicNameInput: '#topic-name',
            topicName: '#topic-name-group'
        },
        events: {
            'click @ui.submitButton': 'onSubmitButtonClick'
        },

        onSubmitButtonClick: function (event) {
            event.preventDefault();
            var topicName = this.ui.topicNameInput.val();

            if (topicName) {
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
                        topic: view.ui.topicNameInput.val()
                    }
                });
            } else {
                $(this.childViewContainer).addClass('hidden-xs-up');
                this.ui.topicName.addClass('has-danger');
            }
        }
    });

    var SegmentLayoutView = Marionette.LayoutView.extend({
        template: false,
        el: 'topic-best-segments-view',
        regions: {
            collectionRegion: '#collection'
        },
        onRender: function () {
            this.collectionRegion.show(new SegmentCollectionView({collection: new SegmentCollection()}));
        }
    });

    TopicsBestSegments.currentView = new SegmentLayoutView();
    TopicsBestSegments.currentView.render();
});