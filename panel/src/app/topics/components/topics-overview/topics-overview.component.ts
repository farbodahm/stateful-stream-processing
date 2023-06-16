import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-topics-overview',
  templateUrl: './topics-overview.component.html',
  styleUrls: ['./topics-overview.component.scss'],
})
export class TopicsOverviewComponent {
  constructor(private _router: Router) {}

  topicDetail(id: any): void {
    this._router.navigate(['/panel/topics/detail'], { queryParams: { id } });
  }
}
