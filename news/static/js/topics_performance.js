app.module("TopicsPerformance", function (TopicsPerformance, NewsChallengeApp, Backbone, Marionette, $, _) {
    var PerformanceModel = Backbone.Model.extend({
        defaults: {
            start: null,
            end: null,
            channel: null
        }
    });

    var PerformanceCollection = Backbone.Collection.extend({
        model: PerformanceModel,
        url: function () {
            return NewsChallengeApp.newsApiUrl + '/topic/performance';
        }
    });

    var NoChildrenView = Marionette.ItemView.extend({
        template: '#empty-template',
        className: 'col-xs-12'
    });

    var PerformanceView = Marionette.ItemView.extend({
        template: '#performance-template',
        className: 'col-xs-12 col-md-6'
    });

    var PerformanceCollectionView = Marionette.CompositeView.extend({
        collection: PerformanceCollection,
        childView: PerformanceView,
        emptyView: NoChildrenView,
        template: '#composite-view-template',
        childViewContainer: '#performances-collection',
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

    var PerformanceLayoutView = Marionette.LayoutView.extend({
        template: false,
        el: 'topic-performance-view',
        regions: {
            collectionRegion: '#collection'
        },
        onRender: function () {
            this.collectionRegion.show(new PerformanceCollectionView({collection: new PerformanceCollection()}));
        }
    });

    TopicsPerformance.currentView = new PerformanceLayoutView();
    TopicsPerformance.currentView.render();
});