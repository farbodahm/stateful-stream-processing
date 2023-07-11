import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TopicsOverviewComponent } from './components/topics-overview/topics-overview.component';
import { TopicDetailComponent } from './components/topic-detail/topic-detail.component';

const ROUTES: Routes = [
  {
    path: '',
    component: TopicsOverviewComponent,
    children: [
      {
        path: 'detail',
        component: TopicDetailComponent,
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(ROUTES)],
  exports: [RouterModule],
})
export class TopicsRoutingModule {}
