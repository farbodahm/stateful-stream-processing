import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Observer } from 'rxjs';
import { AnonymousSubject } from 'rxjs/internal/Subject';
import { Subject } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';

export interface Message {
  source: string;
  content: string;
}

@Injectable({
  providedIn: 'root',
})
export class SocketService {
  private subject!: AnonymousSubject<MessageEvent>;
  public messages: BehaviorSubject<Message[]> = new BehaviorSubject<Message[]>(
    []
  );
  data: Message[] = [];

  constructor() {
    this.connect(environment.socketBase)
      .pipe(
        map((response: MessageEvent): Message => {
          let data = JSON.parse(response.data);
          return data;
        }),
        tap((m) => this.data.push(m)),
        map(() => this.data)
      )
      .subscribe((m: Message[]) => this.messages.next(m));
  }

  public connect(url: string): AnonymousSubject<MessageEvent> {
    if (!this.subject) {
      this.subject = this.create(url);
      console.log('Successfully connected: ' + url);
    }
    return this.subject;
  }

  private create(url: string): AnonymousSubject<MessageEvent> {
    let ws = new WebSocket(url);
    let observable = new Observable((obs: Observer<MessageEvent>) => {
      ws.onmessage = obs.next.bind(obs);
      ws.onerror = obs.error.bind(obs);
      ws.onclose = obs.complete.bind(obs);
      return ws.close.bind(ws);
    });
    let observer: any = {
      next: (data: Object) => {
        console.log('Message sent to websocket: ', data);
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify(data));
        }
      },
    };
    return new AnonymousSubject<MessageEvent>(observer, observable);
  }
}
