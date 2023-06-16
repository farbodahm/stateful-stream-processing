import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { GlobalService } from '@shared/services/global.service';
import { SidenavComponent } from './sidenav.component';
import { StringToUrlPipe } from '@shared/pipes/string-to-url/string-to-url.pipe';
import { HumanCasePipe } from '@shared/pipes/human-case/human-case.pipe';

describe('SidenavComponent', () => {
  let component: SidenavComponent;
  let fixture: ComponentFixture<SidenavComponent>;

  beforeEach(waitForAsync(() => {
    const globalSpy = jasmine.createSpyObj('GlobalService', ['appVersion']);
    globalSpy.appVersion.and.returnValue('0.65.0');

    TestBed.configureTestingModule({
      declarations: [ SidenavComponent ],
      imports: [
        HttpClientTestingModule,
        RouterTestingModule,
      ],
      providers: [
        StringToUrlPipe,
        HumanCasePipe,
        { provide: MatDialog, useValue: {} },
        { provide: MatSnackBar, useValue: {} },
        { provide: GlobalService, useValue: globalSpy },
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SidenavComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
