import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OverviewComponent } from './components/overview/overview.component';
import { DashboardRoutingModule } from './dashboard.routing';
import { NgxJsonViewerModule } from 'ngx-json-viewer';
import { SharedModule } from '../shared/shared.module';

@NgModule({
  declarations: [OverviewComponent],
  imports: [CommonModule, DashboardRoutingModule, NgxJsonViewerModule, SharedModule],
})
export class DashboardModule {}
