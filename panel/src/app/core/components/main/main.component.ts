import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { Router } from '@angular/router';
import { MediaService } from 'src/app/shared/services/media.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {

  @ViewChild('sidenav', { static: true }) sidenav!: MatSidenav;

  public get isMobile(): boolean {
    return this.mediaService.isMobile;
  }

  constructor(
    public mediaService: MediaService,
    private router: Router,
  ) { }

  ngOnInit(): void {
    this.router.events.subscribe(event => {
      if (this.isMobile) {
        this.sidenav.close();
      }
    });
  }
}
