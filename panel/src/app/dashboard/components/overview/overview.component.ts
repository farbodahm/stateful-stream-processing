import { Component } from '@angular/core';
import { SocketService } from 'src/app/shared/services/socket.service';

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss'],
})
export class OverviewComponent {
  constructor(public socketService: SocketService) {}
}
