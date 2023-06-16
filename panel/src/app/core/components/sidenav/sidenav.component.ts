import { Component } from '@angular/core';
import { MultiLevelMenu } from 'src/app/shared/interfaces/multi-level-menu';
import { SIDENAV_CONFIG } from './sidenav.config';

@Component({
  selector: 'app-sidenav',
  templateUrl: './sidenav.component.html',
  styleUrls: ['./sidenav.component.scss'],
})

export class SidenavComponent {

  menuItems: MultiLevelMenu[] = SIDENAV_CONFIG;
  config = {
    paddingAtStart: true,
    interfaceWithRoute: true,
    classname: 'config-sidenav',
    listBackgroundColor: `transparent`,
    fontColor: `#ffffff80`,
    backgroundColor: `transparent`,
    selectedListFontColor: `#ffffff`,
    highlightOnSelect: true,
    collapseOnSelect: false,
    rtlLayout: false,
  };

  public get appItems(): MultiLevelMenu[] {
    return this.menuItems;
  }
}
