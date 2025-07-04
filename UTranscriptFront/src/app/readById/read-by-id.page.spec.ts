import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReadByIdPage } from './read-by-id.page';

describe('ReadByIdPage', () => {
  let component: ReadByIdPage;
  let fixture: ComponentFixture<ReadByIdPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(ReadByIdPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
