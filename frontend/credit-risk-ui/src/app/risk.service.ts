import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RiskService {

  private API_URL = 'https://8081-bbcadfdbafceeafecfefbafaafdfbdaacdcac.premiumproject.examly.io/analyze';

  constructor(private http: HttpClient) {}

  analyze(company: string): Observable<any> {
    return this.http.post(this.API_URL, {
      name: company
    });
  }
}