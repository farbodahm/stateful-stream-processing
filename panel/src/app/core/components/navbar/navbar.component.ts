import { Location } from '@angular/common';
import { Component, EventEmitter, Output } from '@angular/core';
import { MediaService } from 'src/app/shared/services/media.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent {

  @Output() menuClicked = new EventEmitter<void>();

  public get isMobile(): boolean {
    return this.mediaService.isMobile;
  }
  public title!: string;
  public hasBack!: boolean;

  constructor(
    private location: Location,
    public mediaService: MediaService,
  ) { }

  toggleMenu(): void {
    this.menuClicked.emit();
  }

  logout(): void {}

  back(): void {
    // window.history.back();
    this.location.back();
  }
}
