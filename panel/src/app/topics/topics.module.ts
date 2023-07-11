import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TopicsOverviewComponent } from './components/topics-overview/topics-overview.component';
import { TopicsRoutingModule } from './topics.routing';
import { TopicDetailComponent } from './components/topic-detail/topic-detail.component';

@NgModule({
  declarations: [TopicsOverviewComponent, TopicDetailComponent],
  imports: [CommonModule, TopicsRoutingModule],
})
export class TopicsModule {}
