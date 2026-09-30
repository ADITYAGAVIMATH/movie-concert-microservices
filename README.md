\# Movie \& Concert Ticket Booking System



A containerized movie and concert ticket booking system developed using a

microservices architecture.



The project focuses on microservice design, REST-based service communication,

Docker containerization, Docker Compose integration, and performance

evaluation under different workloads.



\---



\## Project Overview



The application is divided into independent microservices, with each service

responsible for a specific business function.



Each microservice has:



\- Its own application code

\- Its own dependencies

\- Its own Dockerfile

\- Its own Docker image

\- Its own container



Docker Compose is used to integrate the services and provide communication

between the containers.



The system will also be evaluated using Locust and a custom Python load

generator under different workloads.



\---



\## Architecture



```text

&#x20;                        Client

&#x20;                          |

&#x20;                          v

&#x20;                   +-------------+

&#x20;                   | API Gateway |

&#x20;                   +------+------+

&#x20;                          |

&#x20;         +----------------+----------------+

&#x20;         |                |                |

&#x20;         v                v                v

&#x20;   +-----------+    +-----------+    +-----------+

&#x20;   |   User    |    |   Event   |    |   Seat    |

&#x20;   |  Service  |    |  Service  |    |  Service  |

&#x20;   +-----------+    +-----------+    +-----------+

&#x20;                          |

&#x20;                          v

&#x20;                   +-------------+

&#x20;                   |   Booking   |

&#x20;                   |   Service   |

&#x20;                   +------+------+

&#x20;                          |

&#x20;                          v

&#x20;                   +-------------+

&#x20;                   |   Payment   |

&#x20;                   |   Service   |

&#x20;                   +-------------+

