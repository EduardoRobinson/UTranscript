import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ReadByIdPage } from './read-by-id.page';

const routes: Routes = [
  {
    path: '',
    component: ReadByIdPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ReadByIdPageRoutingModule {}
