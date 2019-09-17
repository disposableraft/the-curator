import React from 'react';
import {configure, shallow} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import App from './App';

configure({ adapter: new Adapter() });

describe('<App>', () => {
  const defaultState = {
    subject: 'Tadanori Yokoo',
    images: [
      'https://www.moma.org/media/W1siZiIsIjkyODUiXSxbInAiLCJjb252ZXJ0IiwiLXJlc2l6ZSA1MTJ4NTEyXHUwMDNlIl1d.jpg?sha=bcbbfb73f150d6e2',
      'https://www.moma.org/media/W1siZiIsIjkyOTAiXSxbInAiLCJjb252ZXJ0IiwiLXJlc2l6ZSA1MTJ4NTEyXHUwMDNlIl1d.jpg?sha=a6282babc21b9ca9',
      'https://www.moma.org/media/W1siZiIsIjkzMDEiXSxbInAiLCJjb252ZXJ0IiwiLXJlc2l6ZSA1MTJ4NTEyXHUwMDNlIl1d.jpg?sha=233e53a69ab4f422',
    ]
  };

  it('renders renders Artist Name', () => {
    const wrapper = shallow(<App />);
    wrapper.this.state = defaultState;
    expect(wrapper.text()).toBe(defaultState.subject);
  });
  
  it('renders one or more images', () => {
    const wrapper = shallow(<App />);
    expect(wrapper.text()).toBe(<Images />);
    // expect(wrapper.find('.Images').children().length).toBeGreaterThanOrEqual(1);
  });
});


