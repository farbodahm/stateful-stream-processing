import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TopicsOverviewComponent } from './topics-overview.component';

describe('TopicsOverviewComponent', () => {
  let component: TopicsOverviewComponent;
  let fixture: ComponentFixture<TopicsOverviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TopicsOverviewComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TopicsOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
