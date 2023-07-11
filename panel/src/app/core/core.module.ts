import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { MatSidenavModule } from '@angular/material/sidenav';
import { FormsModule } from '@angular/forms';
import { SharedModule } from '../shared/shared.module';
import { MainComponent } from './components/main/main.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { SidenavComponent } from './components/sidenav/sidenav.component';
import { CoreRoutingModule } from './core-routing.module';
import { NotFoundComponent } from './components/not-found/not-found.component';
import { NotAccessComponent } from './components/not-access/not-access.component';
import { MultilevelMenuService, NgMaterialMultilevelMenuModule } from 'ng-material-multilevel-menu';


@NgModule({
  declarations: [
    MainComponent,
    SidenavComponent,
    NavbarComponent,
    NotFoundComponent,
    NotAccessComponent,
  ],
  imports: [
    CommonModule,
    CoreRoutingModule,
    SharedModule,
    MatSidenavModule,
    NgMaterialMultilevelMenuModule,
    FormsModule,
  ],
  providers: [
    MultilevelMenuService,
  ]
})
export class CoreModule { }
