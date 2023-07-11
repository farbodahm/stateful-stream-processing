import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { RouterTestingModule } from '@angular/router/testing';
import { MatMenuModule } from '@angular/material/menu';
import { NavbarComponent } from './navbar.component';

describe('NavbarComponent', () => {
  let component: NavbarComponent;
  let fixture: ComponentFixture<NavbarComponent>;

  beforeEach(waitForAsync(() => {
    const globalSpy = jasmine.createSpyObj('GlobalService', ['appVersion']);
    globalSpy.appVersion.and.returnValue('0.65.0');

    TestBed.configureTestingModule({
      declarations: [ NavbarComponent ],
      imports: [
        RouterTestingModule,
        MatMenuModule,
      ],
      providers: [
        { provide: MatDialog, useValue: {} },
        { provide: MatSnackBar, useValue: {} },
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NavbarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
